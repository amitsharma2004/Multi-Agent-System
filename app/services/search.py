from tavily import TavilyClient
from firecrawl import FirecrawlApp
from app.config import settings

# Initialize clients
tavily_client = TavilyClient(api_key=settings.tavily_api_key)
firecrawl_client = FirecrawlApp(api_key=settings.firecrawl_api_key)


def search_web(query: str, max_results: int = 5):
    """Search the web using Tavily"""
    response = tavily_client.search(query=query, max_results=max_results)
    return response


def scrape_url(url: str):
    """Scrape a URL using Firecrawl"""
    response = firecrawl_client.scrape_url(url)
    return response
