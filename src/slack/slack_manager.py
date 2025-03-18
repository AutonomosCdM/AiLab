# src/slack/slack_manager.py
import logging
from typing import List, Dict, Any, Callable
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .slack_auth import SlackAuth
from .slack_handlers import SlackHandlers

class SlackTool:
    """Representa una herramienta para interactuar con Slack"""
    
    def __init__(self, name: str, description: str, handler: Callable[[str], str]):
        """
        Inicializa una herramienta de Slack
        
        Args:
            name: Nombre de la herramienta
            description: Descripción de la herramienta
            handler: Función que ejecuta la herramienta
        """
        self.name = name
        self.description = description
        self.handler = handler
    
    def run(self, input_text: str) -> str:
        """
        Ejecuta la herramienta
        
        Args:
            input_text: Texto de entrada
            
        Returns:
            Resultado de la ejecución
        """
        return self.handler(input_text)

class SlackManager:
    """Gestiona la integración con Slack"""
    
    def __init__(self):
        """Inicializa el gestor de Slack"""
        self.logger = logging.getLogger("SlackManager")
        self.auth = SlackAuth()
        self.app = None
        self.handlers = None
        self.handler = None
        self.tools = self._create_tools()
    
    def initialize(self, message_processor: Callable[[str], str]) -> App:
        """
        Inicializa la integración con Slack
        
        Args:
            message_processor: Función para procesar mensajes
            
        Returns:
            Instancia de App configurada
        """
        # Crear aplicación Slack
        self.app = self.auth.create_app()
        
        # Registrar manejadores
        self.handlers = SlackHandlers(self.app, message_processor)
        
        return self.app
    
    def start(self) -> None:
        """Inicia la conexión Socket Mode con Slack"""
        if not self.app:
            raise ValueError("Slack app no inicializada. Llama a initialize() primero.")
        
        # Crear y arrancar handler de Socket Mode
        self.handler = self.auth.create_socket_handler(self.app)
        
        self.logger.info("Iniciando conexión Socket Mode con Slack")
        self.handler.start()
    
    def get_tools(self) -> List[SlackTool]:
        """
        Obtiene todas las herramientas disponibles para Slack
        
        Returns:
            Lista de herramientas
        """
        return self.tools
    
    def execute_tool(self, tool_name: str, input_text: str) -> str:
        """
        Ejecuta una herramienta de Slack por nombre
        
        Args:
            tool_name: Nombre de la herramienta
            input_text: Texto de entrada
            
        Returns:
            Resultado de la ejecución
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.run(input_text)
        
        return f"Herramienta '{tool_name}' no encontrada."
    
    def _create_tools(self) -> List[SlackTool]:
        """
        Crea las herramientas disponibles para Slack
        
        Returns:
            Lista de herramientas
        """
        # Ejemplo de herramientas - estas pueden personalizarse
        return [
            SlackTool(
                name="send_message",
                description="Envía un mensaje a un canal o usuario específico. Formato: canal|usuario: mensaje",
                handler=self._handle_send_message
            ),
            SlackTool(
                name="get_channel_info",
                description="Obtiene información sobre un canal. Formato: ID_del_canal",
                handler=self._handle_get_channel_info
            )
        ]
    
    def _handle_send_message(self, input_text: str) -> str:
        """
        Maneja el envío de mensajes a Slack
        
        Args:
            input_text: Formato 'canal|usuario: mensaje'
            
        Returns:
            Confirmación o error
        """
        try:
            if ':' not in input_text:
                return "Formato inválido. Usa 'canal|usuario: mensaje'"
            
            target, message = input_text.split(':', 1)
            target = target.strip()
            message = message.strip()
            
            # Aquí se implementaría la lógica real con el cliente de Slack
            # Por ahora solo devolvemos un mensaje de simulación
            return f"Mensaje enviado a {target}: '{message}'"
        except Exception as e:
            self.logger.error(f"Error al enviar mensaje: {e}")
            return f"Error al enviar mensaje: {str(e)}"
    
    def _handle_get_channel_info(self, channel_id: str) -> str:
        """
        Obtiene información sobre un canal de Slack
        
        Args:
            channel_id: ID del canal
            
        Returns:
            Información del canal o error
        """
        try:
            # Aquí se implementaría la lógica real con el cliente de Slack
            # Por ahora solo devolvemos un mensaje de simulación
            return f"Información del canal {channel_id}: Canal activo con 42 miembros"
        except Exception as e:
            self.logger.error(f"Error al obtener información del canal: {e}")
            return f"Error al obtener información: {str(e)}"
