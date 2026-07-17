import re

COMPLEX_KEYWORDS = [
    "compare", "analyze", "compliance", "gap", "audit", "recommend",
    "why", "explain in detail", "risk assessment", "root cause"
]

def classify_query_complexity(query):
    query_lower = query.lower()
    word_count = len(query.split())

    # Rule 1: Long queries are usually more complex
    if word_count > 25:
        return "complex"

    # Rule 2: Certain keywords signal deep reasoning needed
    if any(keyword in query_lower for keyword in COMPLEX_KEYWORDS):
        return "complex"

    # Rule 3: Multiple questions in one query
    if query_lower.count("?") > 1:
        return "complex"

    return "simple"