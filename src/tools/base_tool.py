# src/tools/base_tool.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseTool(ABC):
    """Clase base para todas las herramientas"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, input_text: str) -> str:
        """
        Ejecuta la herramienta con el texto de entrada proporcionado
        
        Args:
            input_text: Texto de entrada para la herramienta
            
        Returns:
            Resultado de la ejecución como texto
        """
        pass
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convierte la herramienta en un diccionario para serialización
        
        Returns:
            Diccionario con nombre y descripción
        """
        return {
            "name": self.name,
            "description": self.description
        }
