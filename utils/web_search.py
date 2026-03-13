from tavily import TavilyClient
from config.config import TAVILY_API_KEY

def perform_web_search(query: str, max_results: int = 3) -> str:
    if not TAVILY_API_KEY:
        return "(Web search not available — TAVILY_API_KEY missing)"

    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(
            query=query,
            max_results=max_results,
            include_answer=False,
            include_images=False,
        )

        if not response.get("results"):
            return "(No relevant recent results found)"

        formatted = []
        for res in response["results"]:
            title = res.get("title", "No title")
            url = res.get("url", "#")
            content = (res.get("content") or "")[:320].strip()
            formatted.append(f"• **[{title}]({url})**\n  {content}...")

        return "\n\n".join(formatted)

    except Exception as e:
        return f"(Web search error: {str(e)})"
    