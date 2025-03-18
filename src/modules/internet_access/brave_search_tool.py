import os
import requests

class BraveSearchTool:
    def __init__(self, api_key=None):
        """
        Inicializa la herramienta de búsqueda de Brave
        
        Args:
            api_key (str, optional): Clave API de Brave Search. 
                Si no se proporciona, intenta obtenerla de las variables de entorno.
        
        Raises:
            ValueError: Si no se proporciona una clave API válida
        """
        # Validar la clave API
        if api_key is None:
            raise ValueError("Brave Search API key is required")
        
        # Validar que la clave API no sea una cadena vacía
        if api_key == "":
            raise ValueError("Brave Search API key is required")
        
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    def search(self, query, count=5):
        """
        Búsqueda web simple
        
        Args:
            query (str): Consulta de búsqueda
            count (int, optional): Número de resultados. Defecto 5.
        
        Returns:
            dict: Diccionario de resultados con clave 'status'
        """
        # Limpiar la consulta
        query = query.replace('las ultimas', '').replace('últimas', '').strip()
        
        headers = {
            'X-Subscription-Token': self.api_key,
            'Accept': 'application/json'
        }
        
        params = {
            'q': query,
            'count': min(count, 10)  # Limitar a 10 resultados
        }
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            
            # Parsear resultados
            parsed_results = self._parse_results(response.json())
            
            return {
                'status': 'success',
                'results': parsed_results
            }
        
        except requests.exceptions.RequestException as e:
            # Manejar específicamente errores de solicitud
            if e.response and e.response.status_code == 429:
                # Manejar específicamente el error de demasiadas solicitudes
                return {
                    'status': 'error',
                    'error': "Límite de solicitudes alcanzado. Intenta de nuevo más tarde."
                }
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _parse_results(self, data):
        """
        Parsear resultados de manera simple
        
        Args:
            data (dict): Datos brutos de la API de Brave Search
        
        Returns:
            list: Resultados procesados
        """
        results = []
        for item in data.get('web', {}).get('results', []):
            results.append({
                'title': item.get('title', '').replace('<strong>', '').replace('</strong>', ''),
                'url': item.get('url', ''),
                'description': item.get('description', '').replace('<strong>', '').replace('</strong>', '')
            })
        
        return results
    
    def summarize_results(self, search_results):
        """
        Genera un resumen de los resultados de búsqueda
        
        Args:
            search_results (dict): Resultados de búsqueda
        
        Returns:
            str: Resumen de los resultados
        """
        # Manejar caso de error
        if search_results['status'] != 'success':
            return f"Search request failed: {search_results.get('error', 'Unknown error')}"
        
        # Formatear resultados exitosos
        results = search_results['results']
        
        # Generar resumen
        summary = "Resultados de búsqueda:\n\n"
        for i, result in enumerate(results[:3], 1):
            summary += f"{i}. {result['title']}\n"
            summary += f"   {result['description'][:150]}...\n"
            summary += f"   🔗 {result['url']}\n\n"
        
        return summary
    
    def format_results(self, search_results):
        """
        Formatear resultados para presentación
        
        Args:
            search_results (dict): Resultados de búsqueda
        
        Returns:
            str: Resultados formateados
        """
        # Manejar caso de error
        if search_results['status'] != 'success':
            return f"Error en la búsqueda: {search_results.get('error', 'Unknown error')}"
        
        # Formatear resultados exitosos
        results = search_results['results']
        formatted_results = []
        for i, result in enumerate(results[:3], 1):
            formatted_result = f"{i}. **{result['title']}**\n   {result['description'][:150]}...\n   🔗 {result['url']}"
            formatted_results.append(formatted_result)
        
        return "\n\n".join(formatted_results)
