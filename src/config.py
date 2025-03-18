# src/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración centralizada para la aplicación"""
    
    # Credenciales de Slack
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
    
    # Credenciales de servicios LLM
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"
    
    # Credenciales de servicios de búsqueda
    BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
    
    # Configuración del agente
    AGENT_NAME = "Lucius"
    DEFAULT_LANGUAGE = "spanish"
    
    @classmethod
    def validate(cls):
        """Valida que todas las configuraciones necesarias estén presentes"""
        required_vars = [
            "SLACK_BOT_TOKEN", 
            "SLACK_APP_TOKEN", 
            "GROQ_API_KEY", 
            "BRAVE_SEARCH_API_KEY"
        ]
        
        missing = []
        for var in required_vars:
            if not getattr(cls, var):
                missing.append(var)
        
        if missing:
            raise ValueError(f"Faltan variables de configuración: {', '.join(missing)}")
        
        return True

# Validar configuración al importar
if __name__ != "__main__":  # No validar durante tests o ejecución directa
    Config.validate()
