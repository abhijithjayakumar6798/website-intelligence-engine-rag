from backend.retriever import retrieve_chunks
from backend.groq_client import generate_response
from backend.tavily_search import search_web


def ask_question(question):

    matches = retrieve_chunks(question, top_k=10)

    if not matches:
        return {
            "answer": "I could not find that information on the website.",
            "sources": [],
            "source_type": "website"
        }

    top_score = matches[0].score

    # Low confidence -> Tavily fallback
    if top_score < 0.50:

        tavily_result = search_web(question)

        fallback_prompt = f"""
You are a helpful assistant.

Answer the question using the provided web search results.

Context:
{tavily_result["context"]}

Question:
{question}
"""

        answer = generate_response(fallback_prompt)

        return {
            "answer": answer,
            "sources": tavily_result["sources"],
            "source_type": "web"
        }

    # Website retrieval path
    context = "\n\n".join(
        match.metadata["text"]
        for match in matches
    )

    prompt = f"""
You are a website intelligence assistant.

Answer the question using ONLY the provided website context.

Rules:
- Do not invent facts.
- If the answer is not available in the context, say:
  "I could not find that information on the website."
- Provide a concise but complete answer.
- Combine information from multiple context sections when needed.

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
        "sources": sources,
        "source_type": "website"
    }