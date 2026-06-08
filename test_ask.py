from backend.ask import ask_question

response = ask_question(
    "What services does ClaySys provide?"
)

print("\nANSWER:\n")
print(response["answer"])

print("\nSOURCES:\n")

for source in response["sources"]:
    print(source)