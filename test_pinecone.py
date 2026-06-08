from backend.pinecone_manager import index

stats = index.describe_index_stats()

print(stats)