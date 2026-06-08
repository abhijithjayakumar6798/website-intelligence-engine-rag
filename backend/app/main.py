from fastapi import FastAPI
from pydantic import BaseModel

from backend.crawler import crawl_page
from backend.ingest import ingest_website
from backend.ask import ask_question


app = FastAPI(
    title="Website Intelligence Engine"
)


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


@app.post("/crawl")
def crawl_website(request: CrawlRequest):

    return crawl_page(request.url)

@app.post("/ingest")
def ingest(request: IngestRequest):

    return ingest_website(request.url)

@app.post("/ask")
def ask(request: AskRequest):

    return ask_question(request.question)