import json
from groq import Groq
import numpy as np
from app.core.config import settings
from app.db.database import get_connection
from app.services.embeddings import get_embedding

client = Groq(api_key=settings.groq_api_key)

def parse_listing(raw_text: str) -> dict:
    """Use Groq/Llama to extract structured data from a raw post."""
    response = client.chat.completions.create(
        model=settings.llm_model,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": """Extract rental listing details from the post.
Return ONLY a JSON object with these exact keys:
- location: area/neighborhood in Bangalore (string or null)
- rent: monthly rent as integer in INR (integer or null)  
- brokerage: boolean indicating if brokerage is involved (true/false)
- bhk: flat type like '1BHK', '2BHK', '3BHK', 'PG', 'Studio' (string or null)
- amenities: list of amenities mentioned (array of strings, can be empty)
- contact: phone number or contact info (string or null)
No explanation. No markdown. Just the JSON object."""
            },
            {"role": "user", "content": raw_text}
        ]
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if model adds them
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def ingest_listing(raw_text: str, source: str, source_id: str) -> bool:
    """Full pipeline: parse → embed → store. Returns True if new, False if duplicate."""
    try:
        parsed = parse_listing(raw_text)
        embedding = np.array(get_embedding(raw_text), dtype=np.float32)

        conn = get_connection()
        cur = conn.cursor()

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
            parsed.get("brokerage"),
            parsed.get("bhk"),
            parsed.get("amenities", []),
            parsed.get("contact"),
            source_id,
            embedding
        ))

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if result:
            print(f"Ingested: {parsed.get('bhk')} in {parsed.get('location')} "
                  f"@ ₹{parsed.get('rent')}")
            return True
        else:
            print(f"⏭️  Duplicate skipped: {source_id}")
            return False

    except Exception as e:
        print(f"Ingestion error: {e}")
        return False
