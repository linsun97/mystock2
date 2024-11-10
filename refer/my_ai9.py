from duckduckgo_search import DDGS

results = DDGS().text("台灣股市", max_results=5)
print(results)