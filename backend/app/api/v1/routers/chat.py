from fastapi import APIRouter
from groq import Groq
from collections import defaultdict
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag import search_listings, get_listing_stats
from app.core.config import settings

router = APIRouter()
client = Groq(api_key=settings.groq_api_key)

# In-memory session store (per server restart)
sessions: dict = defaultdict(list)

# Entry point for chat interactions
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Retrieve relevant listings via RAG + aggregate stats
    listings = search_listings(request.message, limit=6)
    stats = get_listing_stats()

    # Format as context for LLM
    if listings:
        context_items = []
        for l in listings:
            broker_info = "Listed by Agent (Brokerage applies)" if l.get('brokerage') else "Direct from Owner (No-Broker)"
            amenities_list = ", ".join(l.get('amenities') or ["Not specified"])
            
            item = (
                f"• {l.get('bhk','?')} in {l.get('location','?')} — "
                f"₹{l.get('rent','?')}/mo — "
                f"Status: {broker_info} — "
                f"Amenities: {amenities_list} — "
                f"Contact: {l.get('contact','N/A')} [{l.get('source','?')}]"
            )
            context_items.append(item)
        context = "\n".join(context_items)
    else:
        context = "No listings found in database yet."

    # Build message history
    history = sessions[request.session_id]

    # Format stats summary for LLM awareness
    stats_summary = (
        f"Database overview: {stats['total']} total listings across {stats['areas']} areas. "
        f"Breakdown by area: {stats['by_area']}. "
        f"Average rent: ₹{stats['avg_rent']}/mo."
    )

    messages = [
        {
            "role": "system",
            "content": f"""You are a helpful rental assistant for Bangalore, India.

{stats_summary}

Here are the top matching listings for the user's query:

{context}

Guidelines:
- Be friendly and concise.
- Use the database overview to answer aggregate questions (e.g. "how many listings?", "which areas?").
- Use the top matching listings to answer specific queries (e.g. "find me a 2BHK in Koramangala").
- Mention if a place is 'No-Broker' when relevant.
- List 2-3 key amenities if they match the user's needs.
- If no good match exists, say so honestly and suggest what to look for."""
        },
        *history,
        {"role": "user", "content": request.message}
    ]

    # Get LLM response
    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            temperature=0.7,
            max_tokens=600
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        reply = "Sorry, I'm having trouble connecting to the AI service right now. Please try again in a moment."

    # Update session history (keep last 10 messages)
    sessions[request.session_id].append({"role": "user", "content": request.message})
    sessions[request.session_id].append({"role": "assistant", "content": reply})
    sessions[request.session_id] = sessions[request.session_id][-10:]

    # Serialize listings for the frontend
    for l in listings:
        if l.get("posted_at"):
            l["posted_at"] = str(l["posted_at"])
        if l.get("similarity"):
            l["similarity"] = round(float(l["similarity"]), 3)
        if "brokerage" not in l:
            l["brokerage"] = False

    return ChatResponse(
        reply=reply,
        listings=listings,
        session_id=request.session_id
    )
