# src/modules/tool_manager.py
import logging
from typing import Dict, List, Any
from src.tools.base_tool import BaseTool
from src.tools.search_tool import WebSearchTool

class ToolManager:
    """Gestiona las herramientas disponibles para el agente"""
    
    def __init__(self):
        """Inicializa el gestor de herramientas"""
        self.logger = logging.getLogger("ToolManager")
        self.tools = self._initialize_tools()
    
    def _initialize_tools(self) -> Dict[str, BaseTool]:
        """
        Inicializa todas las herramientas disponibles
        
        Returns:
            Diccionario de herramientas por nombre
        """
        tools = {}
        
        # Registrar herramientas disponibles
        tools_to_register = [
            WebSearchTool()
            # Añadir más herramientas aquí...
        ]
        
        for tool in tools_to_register:
            tools[tool.name] = tool
            self.logger.info(f"Herramienta registrada: {tool.name}")
        
        return tools
    
    def list_tools(self) -> List[str]:
        """
        Lista los nombres de todas las herramientas disponibles
        
        Returns:
            Lista de nombres de herramientas
        """
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> List[Dict[str, str]]:
        """
        Obtiene descripciones de todas las herramientas
        
        Returns:
            Lista de diccionarios con nombre y descripción
        """
        return [tool.to_dict() for tool in self.tools.values()]
    
    def execute_tool(self, tool_name: str, input_text: str) -> str:
        """
        Ejecuta una herramienta específica
        
        Args:
            tool_name: Nombre de la herramienta
            input_text: Texto de entrada
            
        Returns:
            Resultado de la ejecución
        """
        if tool_name not in self.tools:
            self.logger.warning(f"Herramienta no encontrada: {tool_name}")
            return f"Error: Herramienta '{tool_name}' no encontrada."
        
        tool = self.tools[tool_name]
        
        try:
            self.logger.info(f"Ejecutando herramienta {tool_name} con entrada: {input_text}")
            result = tool.execute(input_text)
            return result
        except Exception as e:
            self.logger.error(f"Error al ejecutar herramienta {tool_name}: {e}")
            return f"Error al ejecutar herramienta {tool_name}: {str(e)}"
    
    def search_web(self, query: str, count: int = 3) -> List[Dict[str, str]]:
        """
        Atajo para realizar búsquedas web
        
        Args:
            query: Consulta de búsqueda
            count: Número de resultados
            
        Returns:
            Resultados de búsqueda
        """
        try:
            if "web_search" not in self.tools:
                self.logger.error("Herramienta de búsqueda web no disponible")
                return []
            
            tool = self.tools["web_search"]
            self.logger.info(f"Realizando búsqueda web para: {query}")
            search_client = tool.search_client
            results = search_client.search(query, count=count)
            return results
        except Exception as e:
            self.logger.error(f"Error en búsqueda web: {e}")
            return []
    
    def summarize_search_results(self, results: List[Dict[str, str]]) -> str:
        """
        Genera un resumen de resultados de búsqueda
        
        Args:
            results: Resultados de búsqueda
            
        Returns:
            Resumen formateado
        """
        try:
            if "web_search" not in self.tools:
                self.logger.error("Herramienta de búsqueda web no disponible")
                return "No se pudo generar resumen de búsqueda."
            
            tool = self.tools["web_search"]
            self.logger.info("Generando resumen de resultados de búsqueda")
            search_client = tool.search_client
            summary = search_client.format_results(results)
            return summary
        except Exception as e:
            self.logger.error(f"Error al generar resumen: {e}")
            return f"Error al generar resumen: {str(e)}"
