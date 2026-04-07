# Using Ollama (local)
# import requests
# from app.core.config import settings

# def get_embedding(text: str) -> list[float]:
#     """Embed a document for storage."""
#     response = requests.post(
#         f"{settings.ollama_base_url}/api/embed",
#         json={
#             "model": settings.embedding_model,
#             "input": text
#         }
#     )
#     response.raise_for_status()
#     return response.json()["embeddings"][0]

# def get_query_embedding(text: str) -> list[float]:
#     """Embed a search query — same model, no prefix."""
#     response = requests.post(
#         f"{settings.ollama_base_url}/api/embed",
#         json={
#             "model": settings.embedding_model,
#             "input": text
#         }
#     )
#     response.raise_for_status()
#     return response.json()["embeddings"][0]

# Using Groq (cloud API)
from sentence_transformers import SentenceTransformer

_model = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Embedding model loaded")
    return _model

def get_embedding(text: str) -> list[float]:
    """Embed a document for storage."""
    model = _get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def get_query_embedding(text: str) -> list[float]:
    """Embed a search query — same model as documents."""
    return get_embedding(text)