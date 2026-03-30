import json
import numpy as np
from groq import Groq
from app.core.config import settings
from app.db.database import get_connection
from app.services.embeddings import get_embedding

client = Groq(api_key=settings.groq_api_key)

def parse_listing(raw_text: str) -> dict:
    """Use Groq/Llama to extract structured data from a raw post."""
    try:
        response = client.chat.completions.create(
            model=settings.llm_model,
            temperature=0.1,
            response_format={"type": "json_object"}, # Forces JSON mode if supported by the model
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert at extracting Bangalore rental details.
Return ONLY a JSON object with these exact keys:
- location: specific area in Bangalore (string or null)
- rent: monthly rent as integer in INR (integer or null)  
- brokerage: boolean (true if mentioned, false otherwise)
- bhk: string like '1BHK', '2BHK', 'PG' (string or null)
- amenities: array of strings (e.g. ['Gym', 'Parking'])
- contact: phone/email (string or null)
Strictly no markdown, no preamble."""
                },
                {"role": "user", "content": f"Extract details from this text: {raw_text}"}
            ]
        )

        content = response.choices[0].message.content.strip()
        # Clean potential markdown fences
        if "```" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        
        return json.loads(content)
    except Exception as e:
        print(f"⚠️ LLM Parsing failed: {e}")
        # Return a safe fallback object
        return {"location": None, "rent": None, "brokerage": False, "bhk": None, "amenities": [], "contact": None}

def ingest_listing(raw_text: str, source: str, source_id: str) -> bool:
    """Full pipeline: parse → embed → store. Returns True if new, False if duplicate."""
    try:
        # 1. AI Extraction
        parsed = parse_listing(raw_text)
        
        # 2. Vector Embedding for RAG/Similarity Search
        embedding_list = get_embedding(raw_text)
        embedding = np.array(embedding_list, dtype=np.float32).tolist()

        conn = get_connection()
        cur = conn.cursor()

        # 3. Insert with Conflict Handling
        # Note: Ensure your 'embedding' column in Postgres is of type 'vector'
        cur.execute("""
            INSERT INTO listings 
                (source, raw_text, location, rent, brokerage, bhk, amenities, contact, source_id, embedding)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
            RETURNING id;
        """, (
            source,
            raw_text,
            parsed.get("location"),
            parsed.get("rent"),
            parsed.get("brokerage", False),
            parsed.get("bhk"),
            parsed.get("amenities", []),
            parsed.get("contact"),
            source_id,
            embedding
        ))

        result = cur.fetchone()
        conn.commit()
        
        if result:
            print(f"✨ Ingested: {parsed.get('bhk')} in {parsed.get('location')} @ ₹{parsed.get('rent')}")
            return True
        else:
            print(f"⏭️  Duplicate skipped: {source_id}")
            return False

    except Exception as e:
        print(f"Ingestion pipeline error: {e}")
        if 'conn' in locals(): conn.rollback()
        return False
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()