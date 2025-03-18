# src/tools/search_tool.py
import os
import requests
from typing import Dict, List, Any, Optional
from .base_tool import BaseTool
from src.config import Config

class BraveSearch:
    """Cliente simple para Brave Search API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente con una clave API.
        
        Args:
            api_key: Clave API de Brave Search (opcional)
        """
        self.api_key = api_key or Config.BRAVE_SEARCH_API_KEY
        if not self.api_key:
            raise ValueError("Se requiere una clave API de Brave Search")
        
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    def search(self, query: str, count: int = 3) -> List[Dict[str, str]]:
        """
        Realiza una búsqueda web y devuelve resultados procesados.
        
        Args:
            query: Consulta de búsqueda
            count: Número de resultados (máximo 10)
            
        Returns:
            Lista de resultados con título, url y descripción
        """
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": min(count, 10)  # Limitar a 10 resultados
        }
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extraer y procesar resultados
            results = []
            for item in data.get('web', {}).get('results', []):
                results.append({
                    'title': item.get('title', '').replace('<strong>', '').replace('</strong>', ''),
                    'url': item.get('url', ''),
                    'description': item.get('description', '').replace('<strong>', '').replace('</strong>', '')
                })
            
            return results
            
        except Exception as e:
            print(f"Error en búsqueda Brave: {str(e)}")
            return []
    
    def format_results(self, results: List[Dict[str, str]]) -> str:
        """
        Formatea los resultados para presentación.
        
        Args:
            results: Lista de resultados de búsqueda
            
        Returns:
            Texto formateado con los resultados
        """
        if not results:
            return "No se encontraron resultados"
        
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"{i}. {result['title']}\n   {result['description'][:150]}...\n   {result['url']}")
        
        return "\n\n".join(formatted)

class WebSearchTool(BaseTool):
    """Herramienta para realizar búsquedas web usando Brave Search"""
    
    def __init__(self):
        """Inicializa la herramienta de búsqueda web"""
        super().__init__(
            name="web_search",
            description="Busca información en internet. Útil para encontrar hechos recientes, noticias o información general."
        )
        self.search_client = BraveSearch()
    
    def execute(self, query: str) -> str:
        """
        Ejecuta una búsqueda web
        
        Args:
            query: Consulta de búsqueda
            
        Returns:
            Resultados formateados
        """
        # Limpiar la consulta
        cleaned_query = self._clean_query(query)
        
        if not cleaned_query or len(cleaned_query) < 3:
            return "No se pudo entender la consulta. Por favor proporciona términos de búsqueda más específicos."
        
        # Realizar búsqueda
        results = self.search_client.search(cleaned_query, count=3)
        
        # Formatear y devolver resultados
        if results:
            formatted_results = self.search_client.format_results(results)
            return f"📰 Resultados para: '{cleaned_query}':\n\n{formatted_results}"
        else:
            return f"No se encontraron resultados para '{cleaned_query}'."
    
    def _clean_query(self, query: str) -> str:
        """
        Limpia la consulta de búsqueda
        
        Args:
            query: Consulta original
            
        Returns:
            Consulta limpia
        """
        # Convertir a minúsculas para procesamiento
        query = query.lower()
        
        # Eliminar frases comunes en español
        common_phrases = [
            "puedes buscar", "busca", "buscar", "puedes revisar", "revisar",
            "busca en internet", "encuentra", "encuentra información sobre", 
            "buscar información de", "noticias de", "noticias sobre", 
            "información sobre", "información", "últimas noticias de", 
            "últimas novedades de", "novedades", "qué hay de nuevo en"
        ]
        
        for phrase in common_phrases:
            if phrase in query:
                query = query.replace(phrase, "").strip()
        
        # Eliminar menciones de Slack
        if '<@' in query and '>' in query:
            parts = query.split('>')
            if len(parts) > 1:
                query = parts[1].strip()
        
        return query.strip()
