from backend.retriever import retrieve_chunks
from backend.groq_client import generate_response


def ask_question(question):

    matches = retrieve_chunks(question, top_k=5)

    context = "\n\n".join(
        match.metadata["text"]
        for match in matches
    )

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, say:
"I could not find that information on the website."

Context:
{context}

Question:
{question}
"""

    answer = generate_response(prompt)

    sources = []

    for match in matches:
        url = match.metadata["url"]

        if url not in sources:
            sources.append(url)

    return {
        "answer": answer,
        "sources": sources
    }