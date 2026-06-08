from backend.groq_client import generate_response

response = generate_response(
    "What is Artificial Intelligence?"
)

print(response)