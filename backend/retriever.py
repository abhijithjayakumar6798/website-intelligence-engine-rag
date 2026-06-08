from backend.embedder import get_embedding
from backend.pinecone_manager import index


def retrieve_chunks(query, top_k=10):

    query_embedding = get_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results.matches