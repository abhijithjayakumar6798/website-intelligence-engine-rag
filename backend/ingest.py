from backend.crawler import crawl_page
from backend.embedder import get_embedding
from backend.pinecone_manager import index
from urllib.parse import urlparse


def ingest_website(url):

    if not url.strip():
        return {
            "error": "Please provide a website URL."
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
        website_domain = urlparse(url).netloc

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
    return {
        "pages_crawled": len(pages),
        "chunks_stored": total_chunks
    }