import requests
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup

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

    response = requests.get(request.url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No title found"

    paragraphs = soup.find_all("p")

    content = " ".join(
        p.get_text(strip=True)
        for p in paragraphs
    )

    links = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if href:
            links.append(href)

    return {
        "url": request.url,
        "title": title,
        "content": content[:1000],
        "links": links[:20]
    }