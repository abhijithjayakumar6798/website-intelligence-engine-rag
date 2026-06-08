import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query):

    response = client.search(
        query=query,
        max_results=5
    )

    results = response.get("results", [])

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    sources = [
        result["url"]
        for result in results
    ]

    return {
        "context": context,
        "sources": sources
    }