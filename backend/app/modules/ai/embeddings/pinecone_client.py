from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec

from app.core.config import get_settings

settings = get_settings()

_pinecone_client = None


def get_pinecone_client() -> Pinecone:
    global _pinecone_client
    if _pinecone_client is None:
        _pinecone_client = Pinecone(
            api_key=settings.pinecone_api_key,
            environment=settings.pinecone_environment,
        )
    return _pinecone_client


def get_pinecone_index():
    pc = get_pinecone_client()
    if settings.pinecone_index_name not in pc.list_indexes().names():
        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(settings.pinecone_index_name)


def namespace_for_restaurant(restaurant_id: str) -> str:
    return f"rest_{restaurant_id}"


async def upsert_vectors(restaurant_id: str, vectors: List[Dict[str, Any]]):
    index = get_pinecone_index()
    namespace = namespace_for_restaurant(restaurant_id)
    index.upsert(vectors=vectors, namespace=namespace)


async def delete_vectors_by_ids(restaurant_id: str, ids: List[str]):
    index = get_pinecone_index()
    namespace = namespace_for_restaurant(restaurant_id)
    index.delete(ids=ids, namespace=namespace)


async def query_vectors(restaurant_id: str, vector: List[float], top_k: int = 8) -> List[Dict[str, Any]]:
    index = get_pinecone_index()
    namespace = namespace_for_restaurant(restaurant_id)
    result = index.query(
        vector=vector,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
    )
    return result.matches
