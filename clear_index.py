# clear_index.py

from backend.pinecone_manager import index

index.delete(delete_all=True)

print("All vectors deleted.")