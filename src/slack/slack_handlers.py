# src/slack/slack_handlers.py
import logging
from slack_bolt import App
from typing import Callable

class SlackHandlers:
    """Gestiona los manejadores de eventos de Slack"""
    
    def __init__(self, app: App, message_processor: Callable[[str], str]):
        """
        Inicializa los manejadores de Slack
        
        Args:
            app: Instancia de Slack Bolt App
            message_processor: Función para procesar mensajes
        """
        self.app = app
        self.logger = logging.getLogger("SlackHandlers")
        self.message_processor = message_processor
        
        # Registrar manejadores de eventos
        self._register_handlers()
    
    def _register_handlers(self):
        """Registra todos los manejadores de eventos"""
        self._register_message_handler()
        self._register_app_mention_handler()
    
    def _register_message_handler(self):
        """Registra el manejador para eventos de mensaje"""
        @self.app.event("message")
        def message_handler(body, say, logger):
            logger.info("Evento de mensaje recibido")
            try:
                # Verificar si el mensaje tiene texto y usuario
                if 'text' not in body['event'] or 'user' not in body['event']:
                    return

                user_input = body['event']['text']
                logger.info(f"Entrada del usuario: {user_input}")
                
                # Procesar el mensaje
                response = self.message_processor(user_input)
                
                logger.info(f"Respuesta: {response}")
                say(response)
            except Exception as e:
                logger.error(f"Error en manejador de mensaje: {e}")
    
    def _register_app_mention_handler(self):
        """Registra el manejador para menciones de la aplicación"""
        @self.app.event("app_mention")
        def app_mention_handler(body, say, logger):
            logger.info("Evento de mención recibido")
            try:
                user_input = body['event']['text']
                logger.info(f"Entrada del usuario: {user_input}")
                
                # Procesar el mensaje
                response = self.message_processor(user_input)
                
                logger.info(f"Respuesta: {response}")
                say(response)
            except Exception as e:
                logger.error(f"Error en manejador de mención: {e}")
