"""
Gestor de herramientas para Lucius.
Proporciona una interfaz unificada para acceder a todas las herramientas disponibles.
"""

import os
from typing import Dict, List, Any, Optional

# Importar herramientas
from src.modules.internet_access.brave_search_tool import BraveSearchTool

class ToolManager:
    """
    Gestor de herramientas para Lucius.
    Proporciona una interfaz unificada para acceder a todas las herramientas disponibles.
    """
    
    def __init__(self):
        """
        Inicializa el gestor de herramientas y carga todas las herramientas disponibles.
        """
        self.tools = {}
        self._load_tools()
    
    def _load_tools(self):
        """
        Carga todas las herramientas disponibles.
        """
        # Cargar herramienta de búsqueda web si hay una clave API disponible
        brave_api_key = os.environ.get('BRAVE_SEARCH_API_KEY')
        if brave_api_key:
            try:
                self.tools['web_search'] = BraveSearchTool(brave_api_key)
                print("Herramienta de búsqueda web cargada correctamente.")
            except Exception as e:
                print(f"Error al cargar la herramienta de búsqueda web: {str(e)}")
    
    def get_tool(self, tool_name: str) -> Any:
        """
        Obtiene una herramienta por su nombre.
        
        Args:
            tool_name: Nombre de la herramienta.
            
        Returns:
            La herramienta solicitada o None si no existe.
        """
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """
        Lista todas las herramientas disponibles.
        
        Returns:
            Lista de nombres de herramientas disponibles.
        """
        return list(self.tools.keys())
    
    def search_web(self, query: str, count: int = 5) -> Dict:
        """
        Realiza una búsqueda web.
        
        Args:
            query: Consulta de búsqueda.
            count: Número de resultados a devolver.
            
        Returns:
            Resultados de la búsqueda.
        """
        web_search = self.get_tool('web_search')
        if not web_search:
            return {
                "status": "error",
                "error": "Herramienta de búsqueda web no disponible."
            }
        
        return web_search.search(query, count=count)
    
    def summarize_search_results(self, results: Dict) -> str:
        """
        Genera un resumen de los resultados de búsqueda.
        
        Args:
            results: Resultados de búsqueda.
            
        Returns:
            Resumen de los resultados.
        """
        web_search = self.get_tool('web_search')
        if not web_search:
            return "Herramienta de búsqueda web no disponible."
        
        return web_search.summarize_results(results)
