import requests
from app.core.config import settings

def get_embedding(text: str) -> list[float]:
    """Embed a document — use search_document: prefix for stored listings."""
    response = requests.post(
        f"{settings.ollama_base_url}/api/embed",
        json={
            "model": settings.embedding_model,
            "input": f"search_document: {text}"
        }
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]

def get_query_embedding(text: str) -> list[float]:
    """Embed a search query — use search_query: prefix for better RAG results."""
    response = requests.post(
        f"{settings.ollama_base_url}/api/embed",
        json={
            "model": settings.embedding_model,
            "input": f"search_query: {text}"
        }
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]