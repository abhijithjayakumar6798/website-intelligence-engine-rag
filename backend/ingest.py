from backend.crawler import crawl_page
from backend.embedder import get_embedding
from backend.pinecone_manager import index


def ingest_website(url):
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
                            "text": chunk
                        }
                    }
                ]
            )

            total_chunks += 1

    return {
        "pages_crawled": len(pages),
        "chunks_stored": total_chunks
    }