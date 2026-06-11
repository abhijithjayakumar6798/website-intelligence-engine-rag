import json
import os
from urllib.parse import urlparse
from backend.crawler import crawl_page
from backend.embedder import get_embedding
from backend.pinecone_manager import index


def ingest_website(url):
    if not url.strip():
        return {
            "error": "Please provide a website URL."
        }

    website_domain = urlparse(url).netloc

    # Load cache
    cache_path = "backend/indexed_websites.json"
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
        with open("backend/current_website.txt", "w") as f:
            f.write(matching_key)
        return {
            "pages_crawled": cached_data[matching_key]["pages_crawled"],
            "chunks_stored": cached_data[matching_key]["chunks_stored"]
        }

    """
    Crawl website and store chunks in Pinecone.
    """
    result = crawl_page(url)
    pages = result["pages"]
    total_chunks = 0

    for page in pages:
        page_url = page["url"]
        page_title = page["title"]
        chunks = page["chunks"]

        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            safe_url = page_url.replace("https://", "").replace("/", "_")
            vector_id = f"{safe_url}_{i}"

            index.upsert(
                vectors=[
                    {
                        "id": vector_id,
                        "values": embedding,
                        "metadata": {
                            "url": page_url,
                            "title": page_title,
                            "text": chunk,
                            "website": website_domain
                        }
                    }
                ]
            )
            total_chunks += 1

    with open("backend/current_website.txt", "w") as f:
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