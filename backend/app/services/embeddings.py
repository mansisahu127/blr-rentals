import requests
from app.core.config import settings

def get_embedding(text: str) -> list[float]:
    """Embed a document for storage."""
    response = requests.post(
        f"{settings.ollama_base_url}/api/embed",
        json={
            "model": settings.embedding_model,
            "input": text
        }
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]

def get_query_embedding(text: str) -> list[float]:
    """Embed a search query — same model, no prefix."""
    response = requests.post(
        f"{settings.ollama_base_url}/api/embed",
        json={
            "model": settings.embedding_model,
            "input": text
        }
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]