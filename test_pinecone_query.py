from backend.embedder import get_embedding
from backend.pinecone_manager import index

query = "What services does ClaySys provide?"

query_vector = get_embedding(query)

results = index.query(
    vector=query_vector,
    top_k=3,
    include_metadata=True
)

print(results)