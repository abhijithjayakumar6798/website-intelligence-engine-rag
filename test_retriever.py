from backend.retriever import retrieve_chunks

results = retrieve_chunks(
    "What services does ClaySys provide?"
)

for match in results:
    print("\n---------------------")
    print("Score:", round(match.score, 3))
    print("URL:", match.metadata["url"])
    print("Text:", match.metadata["text"][:250])