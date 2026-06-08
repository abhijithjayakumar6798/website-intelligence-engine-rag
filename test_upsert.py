from backend.embedder import get_embedding
from backend.pinecone_manager import index

text = "Artificial Intelligence helps automate business processes."

vector = get_embedding(text)

index.upsert(
    vectors=[
        {
            "id": "test-1",
            "values": vector,
            "metadata": {
                "text": text
            }
        }
    ]
)

print("Vector inserted successfully")