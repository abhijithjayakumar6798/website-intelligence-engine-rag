# clear_index.py
import os
import json
from backend.pinecone_manager import index

print("Starting index cleanup...")

# Clear Pinecone index
try:
    index.delete(delete_all=True)
    print("All vectors deleted from Pinecone index.")
except Exception as e:
    print(f"Pinecone delete failed: {e}")

# Resolve cache paths relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
indexed_path = os.path.join(BASE_DIR, "backend", "indexed_websites.json")
current_path = os.path.join(BASE_DIR, "backend", "current_website.txt")

# Clear local cache registry
try:
    with open(indexed_path, "w") as f:
        json.dump({}, f, indent=2)
    print("Indexed websites registry (indexed_websites.json) cleared.")
except Exception as e:
    print(f"Failed to clear indexed websites registry: {e}")

# Clear active website tracker
try:
    with open(current_path, "w") as f:
        f.write("")
    print("Current active website cleared.")
except Exception as e:
    print(f"Failed to clear active website tracker: {e}")

print("Index cleanup completed successfully.")