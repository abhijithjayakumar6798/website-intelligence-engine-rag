from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Website Intelligence Engine"
)

class CrawlRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Website Intelligence Engine"
    }


@app.post("/crawl")
def crawl_website(request: CrawlRequest):
    return {
        "message": "URL received successfully",
        "url": request.url
    }