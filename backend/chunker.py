def chunk_text(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks