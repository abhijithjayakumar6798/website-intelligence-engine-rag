from backend.tavily_search import search_web

result = search_web(
    "When was ClaySys founded?"
)

print(result)