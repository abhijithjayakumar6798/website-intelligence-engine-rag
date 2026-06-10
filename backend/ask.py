from backend.retriever import retrieve_chunks
from backend.groq_client import generate_response
from backend.tavily_search import search_web


def ask_question(question):
    with open("backend/current_website.txt", "r") as f:
        current_website = f.read().strip()


    if not question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "source_type": "none"
        }
    
    matches = retrieve_chunks(question, current_website,top_k=10)

    if not matches:
        return {
            "answer": "I could not find that information on the website.",
            "sources": [],
            "source_type": "website"
        }

    top_score = matches[0].score
    print("\n")
    print("=" * 50)
    print("QUESTION:", question)
    print("TOP SCORE:", top_score)

    for i, match in enumerate(matches[:3]):
        print(f"\nMATCH {i+1}")
        print("Score:", match.score)
        print("URL:", match.metadata.get("url"))

    print("=" * 50)
    print("\n")

    # Low confidence -> Tavily fallback
    if top_score < 0.30:

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