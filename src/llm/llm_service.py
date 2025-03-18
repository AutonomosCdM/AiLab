# src/llm/llm_service.py
import logging
from typing import Dict, List, Any, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.config import Config
from .prompt_templates import PromptTemplates

class LLMService:
    """Servicio para comunicación con modelos de lenguaje"""
    
    def __init__(self):
        """Inicializa el servicio LLM"""
        self.logger = logging.getLogger("LLMService")
        
        # Inicializar modelo LLM
        self.llm = self._initialize_llm()
        
        # Historial de conversación (simple)
        self.conversation_history = []
        self.max_history_length = 5
    
    def _initialize_llm(self) -> ChatGroq:
        """
        Inicializa el modelo LLM
        
        Returns:
            Instancia de modelo LLM
        """
        try:
            self.logger.info(f"Inicializando modelo LLM: {Config.GROQ_MODEL}")
            return ChatGroq(
                groq_api_key=Config.GROQ_API_KEY,
                model_name=Config.GROQ_MODEL
            )
        except Exception as e:
            self.logger.error(f"Error al inicializar modelo LLM: {e}")
            raise
    
    def generate_response(self, user_input: str, tools: List[Dict[str, str]]) -> str:
        """
        Genera una respuesta usando el modelo LLM
        
        Args:
            user_input: Entrada del usuario
            tools: Lista de herramientas disponibles
            
        Returns:
            Respuesta generada
        """
        try:
            # Detectar idioma
            language = self._detect_language(user_input)
            
            # Generar prompt de sistema
            system_prompt = PromptTemplates.get_base_system_prompt(tools, language)
            
            # Crear template de prompt
            prompt_messages = [
                ("system", system_prompt),
                ("user", "{input}")
            ]
            prompt = ChatPromptTemplate.from_messages(prompt_messages)
            
            # Crear cadena de procesamiento
            chain = prompt | self.llm
            
            # Generar respuesta
            self.logger.info(f"Generando respuesta para entrada: {user_input}")
            response = chain.invoke({"input": user_input}).content
            
            # Actualizar historial
            self._update_history(user_input, response)
            
            return response
        
        except Exception as e:
            self.logger.error(f"Error al generar respuesta: {e}")
            return f"Disculpa, ocurrió un error: {str(e)}"
    
    def _detect_language(self, text: str) -> str:
        """
        Detecta el idioma del texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Idioma detectado ("spanish" o "english")
        """
        # Indicadores de inglés
        english_indicators = [
            "hello", "hi", "hey", "good morning", "good afternoon",  
            "what's up", "how are you", "help", "need", "please", 
            "thank", "thanks", "would", "could", "should", "may", "might"
        ]
        
        # Verificar indicadores
        text_lower = text.lower()
        for indicator in english_indicators:
            if indicator in text_lower:
                self.logger.info("Detectado idioma: inglés")
                return "english"
        
        # Por defecto, español
        self.logger.info("Detectado idioma: español")
        return "spanish"
    
    def _update_history(self, user_input: str, response: str) -> None:
        """
        Actualiza el historial de conversación
        
        Args:
            user_input: Entrada del usuario
            response: Respuesta generada
        """
        self.conversation_history.append({
            "user_input": user_input,
            "agent_response": response
        })
        
        # Limitar tamaño del historial
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history.pop(0)
