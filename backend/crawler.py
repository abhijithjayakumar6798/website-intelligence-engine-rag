import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def normalize_url(url):
    parsed = urlparse(url)

    domain = parsed.netloc.replace("www.", "")

    return f"{parsed.scheme}://{domain}{parsed.path}"


def crawl_page(url, visited_urls=None, depth=0, max_depth=2):
    if visited_urls is None:
        visited_urls = set()

    url = normalize_url(url)

    
    if url in visited_urls:
        return None
    if depth >= max_depth:
        return {"pages": []}
    visited_urls.add(url)
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc.replace("www.", "")
    print("BASE DOMAIN:", base_domain)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No title found"

    paragraphs = soup.find_all("p")

    content = " ".join(
        p.get_text(strip=True)
        for p in paragraphs
    )

    links = set()
    page_data = {
        "url": url,
        "title": title,
        "content": content[:1000]
    }
    pages = [page_data]

    for link in list(soup.find_all("a"))[:5]:
        href = link.get("href")

        if not href:
            continue

        full_url = urljoin(url, href)
        print("LINK DOMAIN:", urlparse(full_url).netloc)

        link_domain = urlparse(full_url).netloc.replace("www.", "")

        if link_domain == base_domain:
            links.add(full_url)
            print(f"Depth {depth}: {full_url}")
            child_page = crawl_page(full_url, visited_urls, depth + 1, max_depth)

            if child_page:
                pages.extend(child_page["pages"])
    
    return {
    "pages": pages
    }
    

    
