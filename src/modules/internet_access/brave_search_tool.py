import os
import requests
from typing import Dict, List, Optional

class BraveSearchTool:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Brave Search Tool with optional API key.
        If no API key is provided, it will try to read from environment variable.
        """
        # Check if api_key is None or empty string
        if api_key is None or api_key == "":
            raise ValueError("Brave Search API key is required. Set BRAVE_SEARCH_API_KEY environment variable.")
            
        # Use provided API key or environment variable
        self.api_key = api_key.strip() if api_key else os.environ.get('BRAVE_SEARCH_API_KEY', '').strip()
        
        # Double-check that we have a valid API key
        if not self.api_key:
            raise ValueError("Brave Search API key is required. Set BRAVE_SEARCH_API_KEY environment variable.")
        
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }

    def search(self, query: str, count: int = 5, offset: int = 0) -> Dict:
        """
        Perform a web search using Brave Search API.
        
        Args:
            query (str): Search query
            count (int, optional): Number of results to return. Defaults to 5.
            offset (int, optional): Pagination offset. Defaults to 0.
        
        Returns:
            Dict containing search results
        """
        params = {
            "q": query,
            "count": min(count, 20),  # Max 20 results per request
            "offset": offset
        }

        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            return self._parse_results(response.json())
        
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Search request failed: {str(e)}",
                "status": "error"
            }

    def _parse_results(self, raw_results: Dict) -> Dict:
        """
        Parse and format raw Brave Search API results.
        
        Args:
            raw_results (Dict): Raw JSON results from Brave Search API
        
        Returns:
            Dict with parsed and formatted results
        """
        try:
            results = []
            for result in raw_results.get('web', {}).get('results', []):
                results.append({
                    "title": result.get('title', ''),
                    "url": result.get('url', ''),
                    "description": result.get('description', '')
                })
            
            return {
                "status": "success",
                "query": raw_results.get('query', ''),
                "total_results": raw_results.get('web', {}).get('total', 0),
                "results": results
            }
        
        except Exception as e:
            return {
                "error": f"Error parsing search results: {str(e)}",
                "status": "error"
            }

    def summarize_results(self, results: Dict, max_results: int = 3) -> str:
        """
        Generate a concise summary of search results.
        
        Args:
            results (Dict): Search results from search method
            max_results (int, optional): Maximum number of results to include. Defaults to 3.
        
        Returns:
            str: Summarized search results
        """
        if results.get('status') != 'success':
            return results.get('error', 'Search failed.')
        
        summary_parts = []
        for result in results['results'][:max_results]:
            summary_parts.append(f"• {result['title']}: {result['description'][:100]}...")
        
        return f"Resultados de búsqueda para '{results['query']}':\n" + "\n".join(summary_parts)
