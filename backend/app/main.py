import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.crawler import crawl_page
from backend.ingest import ingest_website
from backend.ask import ask_question


app = FastAPI(
    title="Website Intelligence Engine"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEXED_PATH = os.path.join(BASE_DIR, "indexed_websites.json")
CURRENT_PATH = os.path.join(BASE_DIR, "current_website.txt")

class CrawlRequest(BaseModel):
    url: str
class IngestRequest(BaseModel):
    url: str
class AskRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Website Intelligence Engine"
    }


@app.get("/indexed_websites")
def get_indexed_websites():
    try:
        with open(INDEXED_PATH, "r") as f:
            indexed = json.load(f)
    except Exception as e:
        indexed = {}

    active = ""
    try:
        with open(CURRENT_PATH, "r") as f:
            active = f.read().strip()
    except Exception as e:
        pass

    return {
        "indexed": indexed,
        "active": active
    }


@app.delete("/indexed_websites/{domain}")
def delete_indexed_website(domain: str):
    # Deleting from Pinecone
    try:
        from backend.pinecone_manager import index
        
        # Deleting matching metadata
        index.delete(filter={"website": domain})
        if domain.startswith("www."):
            index.delete(filter={"website": domain.replace("www.", "")})
        else:
            index.delete(filter={"website": f"www.{domain}"})
    except Exception as e:
        print(f"Error deleting from Pinecone for domain {domain}: {e}")
        # Continue to clear registry even if Pinecone fails or is already empty

    # Update cache
    try:
        if os.path.exists(INDEXED_PATH):
            with open(INDEXED_PATH, "r") as f:
                cached_data = json.load(f)
        else:
            cached_data = {}
    except Exception as e:
        cached_data = {}

    updated_data = {}
    for key, val in cached_data.items():
        k_clean = key.replace("www.", "").lower()
        d_clean = domain.replace("www.", "").lower()
        if k_clean != d_clean:
            updated_data[key] = val

    try:
        with open(INDEXED_PATH, "w") as f:
            json.dump(updated_data, f, indent=2)
    except Exception as e:
        print("Error saving indexed_websites.json:", e)

    # Check and clear active website selection
    try:
        if os.path.exists(CURRENT_PATH):
            with open(CURRENT_PATH, "r") as f:
                active = f.read().strip()
            
            a_clean = active.replace("www.", "").lower()
            d_clean = domain.replace("www.", "").lower()
            if a_clean == d_clean:
                with open(CURRENT_PATH, "w") as f:
                    f.write("")
    except Exception as e:
        pass

    return {"status": "deleted", "domain": domain}


@app.post("/crawl")
def crawl_website(request: CrawlRequest):

    return crawl_page(request.url)

@app.post("/ingest")
def ingest(request: IngestRequest):

    return ingest_website(request.url)

@app.post("/ask")
def ask(request: AskRequest):

    return ask_question(request.question)