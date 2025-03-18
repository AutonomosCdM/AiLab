# src/lucius_agent.py
import os
import sys
import logging
from typing import Dict, List, Any, Optional

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Importar componentes base
from agent_base import AgentBase

# Importar servicios y managers
from src.llm.llm_service import LLMService
from src.slack.slack_manager import SlackManager
from src.modules.tool_manager import ToolManager

# Importar configuración
from src.config import Config

class LuciusAgent(AgentBase):
    """Implementación del agente Lucius"""
    
    def __init__(self, name: str = "Lucius"):
        """
        Inicializa el agente Lucius
        
        Args:
            name: Nombre del agente
        """
        super().__init__(name)
        
        # Configurar logging
        self.logger = logging.getLogger("LuciusAgent")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Inicializar servicios y managers
        self.tool_manager = ToolManager()
        self.llm_service = LLMService()
        self.slack_manager = SlackManager()
        
        # Habilitar capacidades
        self.enable_capability("web_search")
        self.enable_capability("slack_integration")
    
    def handle_message(self, user_input: str) -> str:
        """
        Procesa un mensaje de usuario y genera una respuesta
        
        Args:
            user_input: Mensaje del usuario
            
        Returns:
            Respuesta del agente
        """
        self.logger.info(f"Procesando mensaje: {user_input}")
        
        # Detectar y manejar comandos de herramientas
        if user_input.startswith("tool_code"):
            return self._handle_tool_command(user_input)
        
        # Detectar solicitud de búsqueda
        if self._is_search_request(user_input) and self.has_capability("web_search"):
            return self._handle_search_request(user_input)
        
        # Generar respuesta usando LLM
        tool_descriptions = self.tool_manager.get_tool_descriptions()
        response = self.llm_service.generate_response(user_input, tool_descriptions)
        
        # Guardar contexto
        self.memory_manager.save_context(user_input, response)
        
        return response
    
    def initialize_slack(self) -> None:
        """Inicializa la integración con Slack"""
        if not self.has_capability("slack_integration"):
            self.logger.warning("Integración de Slack no habilitada")
            return
        
        try:
            self.logger.info("Inicializando integración con Slack")
            
            # Inicializar app de Slack con procesador de mensajes
            self.slack_manager.initialize(self.handle_message)
            
            # Iniciar conexión Socket Mode
            self.slack_manager.start()
            
            self.logger.info("Integración con Slack inicializada")
        except Exception as e:
            self.logger.error(f"Error al inicializar Slack: {e}")
            raise
    
    def _handle_tool_command(self, command_text: str) -> str:
        """
        Procesa un comando de herramienta
        
        Args:
            command_text: Texto del comando
            
        Returns:
            Resultado de la ejecución
        """
        try:
            # Extraer nombre de herramienta y entrada
            tool_code_block = command_text.split("```tool_code")[1].split("```")[0].strip()
            tool_name, tool_input = tool_code_block.split(":", 1)
            tool_name = tool_name.strip()
            tool_input = tool_input.strip()
            
            self.logger.info(f"Ejecutando herramienta: {tool_name}")
            
            # Ejecutar herramienta
            result = self.tool_manager.execute_tool(tool_name, tool_input)
            
            return result
        except Exception as e:
            self.logger.error(f"Error al procesar comando de herramienta: {e}")
            return f"Error al procesar comando: {str(e)}"
    
    def _is_search_request(self, text: str) -> bool:
        """
        Determina si un texto es una solicitud de búsqueda
        
        Args:
            text: Texto a analizar
            
        Returns:
            True si es una solicitud de búsqueda
        """
        search_indicators = [
            "busca", "buscar", "encuentra", "revisar", "noticias", 
            "información", "novedades", "internet"
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in search_indicators)
    
    def _handle_search_request(self, text: str) -> str:
        """
        Maneja una solicitud de búsqueda
        
        Args:
            text: Texto de la solicitud
            
        Returns:
            Resultados de búsqueda
        """
        try:
            # Extraer términos de búsqueda
            search_query = self._extract_search_query(text)
            
            if not search_query or len(search_query) < 3:
                return "No entendí qué quieres buscar. Por favor sé más específico."
            
            self.logger.info(f"Realizando búsqueda para: {search_query}")
            
            # Ejecutar búsqueda
            results = self.tool_manager.search_web(search_query, count=3)
            
            # Formatear resultados
            if results:
                summary = self.tool_manager.summarize_search_results(results)
                return f"📰 Resultados para: '{search_query}':\n\n{summary}"
            else:
                return f"No encontré resultados para '{search_query}'."
        
        except Exception as e:
            self.logger.error(f"Error en búsqueda web: {e}")
            return f"Ocurrió un error al realizar la búsqueda: {str(e)}"
    
    def _extract_search_query(self, text: str) -> str:
        """
        Extrae términos de búsqueda de un texto
        
        Args:
            text: Texto original
            
        Returns:
            Términos de búsqueda
        """
        query = text.lower()
        
        # Eliminar frases comunes
        common_phrases = [
            "puedes buscar", "puedes revisar", "busca en internet",
            "encuentra información sobre", "buscar información de",
            "noticias de", "noticias sobre", "información sobre",
            "últimas noticias de", "últimas novedades de", "busca",
            "buscar", "encuentra", "revisar", "información", "novedades"
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

def main():
    """Función principal para iniciar el agente"""
    try:
        # Verificar configuración
        Config.validate()
        
        # Inicializar agente
        lucius = LuciusAgent()
        
        # Inicializar integración con Slack si se requiere
        if os.environ.get("START_SLACK", "true").lower() == "true":
            lucius.initialize_slack()
        else:
            # Modo interactivo para pruebas
            print(f"Agente {lucius.name} iniciado en modo interactivo")
            print("Escribe 'exit' para salir")
            
            while True:
                user_input = input("> ")
                if user_input.lower() == "exit":
                    break
                
                response = lucius.handle_message(user_input)
                print(f"\n{lucius.name}: {response}\n")
    
    except Exception as e:
        logging.error(f"Error al iniciar el agente: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()
