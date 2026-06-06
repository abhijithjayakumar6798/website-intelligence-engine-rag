import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def crawl_page(url):

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No title found"

    paragraphs = soup.find_all("p")

    content = " ".join(
        p.get_text(strip=True)
        for p in paragraphs
    )

    links = set()

    for link in soup.find_all("a"):
        href = link.get("href")

        if not href:
            continue

        full_url = urljoin(url, href)

        if urlparse(full_url).netloc == base_domain:
            links.add(full_url)

    return {
        "url": url,
        "title": title,
        "content": content[:1000],
        "links": list(links)[:20]
    }