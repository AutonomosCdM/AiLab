import os
import requests
from typing import Dict, Optional, Any

class BraveSearch:
    """
    Simple wrapper for Brave Search API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize with API key.
        """
        self.api_key = api_key or os.environ.get('BRAVE_SEARCH_API_KEY')
        if not self.api_key:
            raise ValueError("Brave Search API key is required")
        
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }
    
    def search(self, query: str, count: int = 3) -> Dict[str, Any]:
        """
        Perform a web search.
        
        Args:
            query: Search query
            count: Number of results to return
            
        Returns:
            Raw search results
        """
        params = {
            "q": query,
            "count": min(count, 10)  # Limit to 10 results
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Brave Search error: {str(e)}")
            return {"error": str(e)}
