import json
import os
import math
import time
from urllib.parse import urlparse
from backend.crawler import crawl_page
from backend.embedder import get_embeddings
from backend.pinecone_manager import index


def ingest_website(url):
    if not url.strip():
        return {
            "error": "Please provide a website URL."
        }

    website_domain = urlparse(url).netloc

    # Load cache
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    cache_path = os.path.join(BASE_DIR, "indexed_websites.json")
    current_path = os.path.join(BASE_DIR, "current_website.txt")
    cached_data = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cached_data = json.load(f)
        except Exception as e:
            print("Error loading indexed_websites.json:", e)

    # Check if domain exists in the cache
    matching_key = None
    for key in cached_data:
        k_clean = key.replace("www.", "")
        d_clean = website_domain.replace("www.", "")
        if k_clean == d_clean:
            matching_key = key
            break

    if matching_key:
        with open(current_path, "w") as f:
            f.write(matching_key)
        return {
            "pages_crawled": cached_data[matching_key]["pages_crawled"],
            "chunks_stored": cached_data[matching_key]["chunks_stored"]
        }

    print("Starting ingestion...")
    total_start_time = time.time()

    # Crawling website
    result = crawl_page(url)
    pages = result.get("pages", [])
    print(f"Pages crawled: {len(pages)}")

    # Flatten chunks
    flat_chunks = []
    for page in pages:
        page_url = page.get("url", "")
        page_title = page.get("title", "")
        chunks = page.get("chunks", [])
        for i, chunk in enumerate(chunks):
            flat_chunks.append({
                "text": chunk,
                "url": page_url,
                "title": page_title,
                "index": i
            })

    total_chunks = len(flat_chunks)
    print(f"Chunks generated: {total_chunks}")

    if total_chunks == 0:
        return {
            "pages_crawled": len(pages),
            "chunks_stored": 0
        }

    # Batch embedding generation
    print("Generating embeddings...")
    embed_start_time = time.time()
    embeddings = []
    texts = [item["text"] for item in flat_chunks]
    
    embed_batch_size = 32
    total_embed_batches = math.ceil(total_chunks / embed_batch_size)
    
    for i in range(0, total_chunks, embed_batch_size):
        batch_texts = texts[i:i + embed_batch_size]
        batch_num = (i // embed_batch_size) + 1
        print(f"Embedding batch {batch_num}/{total_embed_batches}")
        
        batch_embeddings = get_embeddings(batch_texts, batch_size=embed_batch_size)
        embeddings.extend(batch_embeddings)
        
    embed_time = time.time() - embed_start_time

    # Build Pinecone vectors list
    vectors = []
    for item, embedding in zip(flat_chunks, embeddings):
        page_url = item["url"]
        safe_url = page_url.replace("https://", "").replace("/", "_")
        vector_id = f"{safe_url}_{item['index']}"
        
        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "url": page_url,
                "title": item["title"],
                "text": item["text"],
                "website": website_domain
            }
        })

    # Batch Pinecone upserting
    print("Uploading vectors...")
    upsert_start_time = time.time()
    
    upsert_batch_size = 100
    total_upsert_batches = math.ceil(total_chunks / upsert_batch_size)
    
    for i in range(0, total_chunks, upsert_batch_size):
        batch = vectors[i:i + upsert_batch_size]
        batch_num = (i // upsert_batch_size) + 1
        print(f"Upsert batch {batch_num}/{total_upsert_batches}")
        
        index.upsert(vectors=batch)
        
    upsert_time = time.time() - upsert_start_time
    total_ingest_time = time.time() - total_start_time

    # Print performance log summary
    print("\n--- Ingestion Performance ---")
    print(f"Total chunks: {total_chunks}")
    print(f"Embedding time: {embed_time:.2f} sec")
    print(f"Upsert time: {upsert_time:.2f} sec")
    print(f"Total ingestion time: {total_ingest_time:.2f} sec")
    print("-----------------------------\n")
    print("Ingestion complete.")

    with open(current_path, "w") as f:
        f.write(website_domain)

    # Save new website to cache
    cached_data[website_domain] = {
        "url": url,
        "pages_crawled": len(pages),
        "chunks_stored": total_chunks
    }
    try:
        with open(cache_path, "w") as f:
            json.dump(cached_data, f, indent=2)
    except Exception as e:
        print("Error saving indexed_websites.json:", e)

    return {
        "pages_crawled": len(pages),
        "chunks_stored": total_chunks
    }