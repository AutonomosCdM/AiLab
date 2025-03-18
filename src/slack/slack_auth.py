# src/slack/slack_auth.py
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.config import Config

class SlackAuth:
    """Maneja la autenticación y conexión con Slack"""
    
    def __init__(self):
        """Inicializa la autenticación de Slack"""
        self.logger = logging.getLogger("SlackAuth")
        
        # Configurar logging básico si no está configurado
        if not logging.getLogger().handlers:
            logging.basicConfig(level=logging.INFO)
    
    def create_app(self) -> App:
        """
        Crea y configura la aplicación Slack Bolt
        
        Returns:
            Instancia de App configurada
        """
        try:
            self.logger.info("Inicializando aplicación Slack Bolt")
            app = App(token=Config.SLACK_BOT_TOKEN)
            return app
        except Exception as e:
            self.logger.error(f"Error al inicializar Slack Bolt app: {e}")
            raise
    
    def create_socket_handler(self, app: App) -> SocketModeHandler:
        """
        Crea un handler para Socket Mode
        
        Args:
            app: Instancia de Slack Bolt App
            
        Returns:
            Handler configurado para Socket Mode
        """
        try:
            self.logger.info("Inicializando Socket Mode Handler")
            handler = SocketModeHandler(app, Config.SLACK_APP_TOKEN)
            return handler
        except Exception as e:
            self.logger.error(f"Error al inicializar Socket Mode Handler: {e}")
            raise
