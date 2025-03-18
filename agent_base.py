# src/agent_base.py
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class MemoryManager:
    """Gestiona el almacenamiento de contexto y memoria del agente"""
    
    def __init__(self):
        """Inicializa el gestor de memoria"""
        self.context = {}
        self.conversation_history = []
    
    def save_context(self, user_input: str, agent_response: str) -> None:
        """
        Guarda contexto de conversación
        
        Args:
            user_input: Entrada del usuario
            agent_response: Respuesta del agente
        """
        self.conversation_history.append({
            "user_input": user_input,
            "agent_response": agent_response
        })
        
        # Limitar tamaño del historial
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de contexto
        
        Args:
            key: Clave de contexto
            default: Valor por defecto si no existe
            
        Returns:
            Valor almacenado o valor por defecto
        """
        return self.context.get(key, default)
    
    def set_context(self, key: str, value: Any) -> None:
        """
        Establece un valor de contexto
        
        Args:
            key: Clave de contexto
            value: Valor a almacenar
        """
        self.context[key] = value
    
    def get_recent_history(self, count: int = 3) -> List[Dict[str, str]]:
        """
        Obtiene historial reciente de conversación
        
        Args:
            count: Número de entradas a recuperar
            
        Returns:
            Lista de entradas recientes
        """
        return self.conversation_history[-count:] if self.conversation_history else []

class AgentBase(ABC):
    """Clase base para agentes de IA"""
    
    def __init__(self, name: str):
        """
        Inicializa el agente base
        
        Args:
            name: Nombre del agente
        """
        self.name = name
        self.memory_manager = MemoryManager()
        self.capabilities = set()
    
    @abstractmethod
    def handle_message(self, user_input: str) -> str:
        """
        Procesa un mensaje de usuario y genera una respuesta
        
        Args:
            user_input: Mensaje del usuario
            
        Returns:
            Respuesta del agente
        """
        pass
    
    def enable_capability(self, capability: str) -> None:
        """
        Habilita una capacidad
        
        Args:
            capability: Nombre de la capacidad
        """
        self.capabilities.add(capability)
    
    def disable_capability(self, capability: str) -> None:
        """
        Deshabilita una capacidad
        
        Args:
            capability: Nombre de la capacidad
        """
        if capability in self.capabilities:
            self.capabilities.remove(capability)
    
    def has_capability(self, capability: str) -> bool:
        """
        Verifica si una capacidad está habilitada
        
        Args:
            capability: Nombre de la capacidad
            
        Returns:
            True si la capacidad está habilitada
        """
        return capability in self.capabilities
