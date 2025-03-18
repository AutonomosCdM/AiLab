import json
import os
import random
from typing import List, Dict, Any

class PersonalityManager:
    def __init__(self, personalities_dir="src/modules/personalities/", default_personality_name="lucius_fox"):
        self.personalities_dir = personalities_dir
        self.personalities = self._load_personalities(default_personality_name)
        self.active_personality_name = default_personality_name
        self.conversation_context = []
        self.max_context_length = 5  # Limit context to last 5 interactions

    def _load_personalities(self, default_personality_name=None):
        """
        Carga todas las personalidades disponibles en el directorio especificado.
        
        Args:
            default_personality_name: Nombre de la personalidad predeterminada a activar
        
        Returns:
            Dict con todas las personalidades cargadas
        """
        personalities = {}
        
        # Verificar que el directorio existe
        if not os.path.exists(self.personalities_dir):
            print(f"El directorio de personalidades no existe: {self.personalities_dir}")
            return self._create_default_personality()
        
        # Cargar todos los archivos JSON del directorio
        for filename in os.listdir(self.personalities_dir):
            if filename.endswith('.json'):
                personality_name = filename[:-5]  # Eliminar la extensión .json
                filepath = os.path.join(self.personalities_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        personality_data = json.load(f)
                        personalities[personality_name] = personality_data
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Error al decodificar {filename}: {str(e)}")
        
        # Si no se encontraron personalidades o la predeterminada no existe
        if not personalities or (default_personality_name and default_personality_name not in personalities):
            print("No se encontraron personalidades válidas o la personalidad predeterminada no existe")
            default_personality = self._create_default_personality()
            personalities['default'] = default_personality['default']
        
        return personalities

    def _create_default_personality(self):
        """
        Crea una personalidad predeterminada en caso de que no se encuentre ninguna.
        
        Returns:
            Dict con una personalidad predeterminada
        """
        return {
            'default': {
                "name": "default",
                "description": "Default personality with a helpful and concise tone.",
                "traits": ["helpful", "professional", "concise"],
                "tone": "neutral",
                "verbosity": "Concise",
                "phrases": ["Tecnología no es magia."]
            }
        }

    def set_active_personality(self, personality_name):
        """
        Cambia la personalidad activa.
        
        Args:
            personality_name: Nombre de la personalidad a activar
        
        Returns:
            bool: True si se activó correctamente, False en caso contrario
        """
        if personality_name in self.personalities:
            self.active_personality_name = personality_name
            return True
        else:
            print(f"La personalidad '{personality_name}' no existe")
            return False

    def list_available_personalities(self):
        """
        Lista todas las personalidades disponibles.
        
        Returns:
            List de nombres de personalidades
        """
        return list(self.personalities.keys())

    def update_conversation_context(self, user_input: str, agent_response: str):
        """
        Update conversation context while maintaining a sliding window
        """
        context_entry = {
            "user_input": user_input,
            "agent_response": agent_response
        }
        
        # Add new context entry
        self.conversation_context.append(context_entry)
        
        # Maintain maximum context length
        if len(self.conversation_context) > self.max_context_length:
            self.conversation_context.pop(0)

    def generate_dynamic_system_prompt(self, base_prompt: str) -> str:
        """
        Generate a dynamic system prompt based on conversation context
        """
        personality = self.get_active_personality()
        
        # Extract key context elements
        context_summary = self._summarize_context()
        
        # Dynamic trait selection based on context
        dynamic_traits = self._select_dynamic_traits(context_summary)
        
        # Construct enhanced system prompt
        dynamic_prompt = f"""{base_prompt}

Conversation Context Summary:
{context_summary}

Dynamic Personality Traits to Emphasize:
{', '.join(dynamic_traits)}

Communication Guidelines:
- Maintain a concise and technically precise tone
- Adapt responses based on the conversation's evolving context
- Preserve the core personality while being contextually responsive
"""
        return dynamic_prompt

    def _summarize_context(self) -> str:
        """
        Create a brief summary of recent conversation context
        """
        if not self.conversation_context:
            return "No recent conversation context."
        
        summary_parts = []
        for entry in self.conversation_context[-3:]:  # Use last 3 interactions
            summary_parts.append(f"User asked: {entry['user_input']}")
        
        return "\n".join(summary_parts)

    def _select_dynamic_traits(self, context_summary: str) -> List[str]:
        """
        Dynamically select personality traits based on conversation context
        """
        personality = self.get_active_personality()
        base_traits = personality.get('traits', [])

        # Context-based trait modulation
        dynamic_traits = base_traits.copy()

        # Limitar la influencia del contexto en la personalidad
        
        if "tecnología" in context_summary.lower():
            dynamic_traits.append("technical_focus")
        
        # 🚨 Eliminar "ethical_consideration" si no es estrictamente necesario
        if "ética" in context_summary.lower():
            if "pregunta específica sobre ética" in context_summary.lower():  # Agrega más control
                dynamic_traits.append("ethical_consideration")

        return list(set(dynamic_traits))  # Remove duplicates

    def get_active_personality(self):
        return self.personalities.get(self.active_personality_name)

    def _apply_verbosity(self, response: str, personality: dict) -> str:
        """
        Aplica el nivel de verbosidad a la respuesta.
        """
        verbosity = personality.get('verbosity', 'Concise')

        # Dividir en oraciones y preservar la puntuación
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        
        if not sentences:
            return response
            
        if verbosity == 'Ultra-concise':
            # Solo la primera oración, y si es muy larga, solo la primera parte
            first_sentence = sentences[0]
            if len(first_sentence) > 80:  # Si es muy larga
                parts = first_sentence.split(',')
                if len(parts) > 1:
                    return parts[0] + '.'
            return first_sentence + '.'
            
        elif verbosity == 'Concise':
            # Máximo 1 oración para respuestas normales
            if len(sentences) > 0:
                return sentences[0] + '.'
            
        # Para otros niveles de verbosidad, mantener la respuesta original
        return response

    def _apply_tone(self, response: str, personality: dict) -> str:
        """
        Aplica el tono de voz a la respuesta.
        """
        tone = personality.get('tone', 'neutral')

        if tone == 'sharp_wit':
            phrases = personality.get('phrases', [])
            # Reducir la probabilidad de añadir frases a solo 10% y solo si no es una pregunta
            # y la respuesta no es demasiado larga
            if phrases and "?" not in response and len(response) < 60 and random.random() < 0.1:
                response += " " + random.choice(phrases)

        elif tone == 'professional':
            # Eliminar expresiones demasiado informales o emojis
            response = response.replace('!', '.').replace('?!', '?')

        elif tone == 'friendly':
            # Potencialmente añadir un toque amigable
            if random.random() < 0.2 and not response.endswith('!'):
                response = response.rstrip('.') + '!'

        return response

    def _apply_context_patterns(self, response: str) -> str:
        """
        Aplica patrones basados en el contexto de la conversación.
        """
        # Si no hay contexto, devolver la respuesta sin cambios
        if not self.conversation_context:
            return response
        
        # Analizar patrones en el contexto reciente
        recent_context = self.conversation_context[-1]
        user_input = recent_context.get('user_input', '').lower()
        
        # Ejemplo: Si el usuario hace una pregunta corta, asegurar respuesta directa
        if len(user_input.split()) <= 5 and user_input.endswith('?'):
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            if sentences:
                return sentences[0] + '.'
        
        return response

    def _extract_topics(self) -> List[str]:
        """
        Extrae temas recurrentes de las conversaciones.
        
        Returns:
            Lista de temas identificados
        """
        # Implementación simple basada en palabras clave
        keywords = {
            "tecnología": ["tecnología", "tech", "dispositivo", "software", "hardware"],
            "ética": ["ética", "moral", "valores", "principios"],
            "negocio": ["negocio", "empresa", "corporación", "financiero"],
            "ayuda": ["ayuda", "asistencia", "apoyo", "solución"]
        }
        
        all_text = " ".join([
            entry['user_input'].lower() + " " + entry['agent_response'].lower()
            for entry in self.conversation_context
        ])
        
        found_topics = []
        for topic, words in keywords.items():
            if any(word in all_text for word in words):
                found_topics.append(topic)
        
        return found_topics or ["general conversation"]

    def _detect_sentiment(self) -> str:
        """
        Detecta el sentimiento general de la conversación.
        
        Returns:
            String con el sentimiento detectado
        """
        # Implementación simple basada en palabras clave
        positive_words = ["gracias", "excelente", "genial", "bueno", "me gusta"]
        negative_words = ["mal", "error", "problema", "difícil", "no funciona"]
        
        all_user_text = " ".join([
            entry['user_input'].lower() for entry in self.conversation_context
        ])
        
        positive_count = sum(1 for word in positive_words if word in all_user_text)
        negative_count = sum(1 for word in negative_words if word in all_user_text)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def transform_response(self, response: str) -> str:
        """
        Transforma la respuesta según la personalidad activa.

        Args:
            response: Texto de respuesta original

        Returns:
            Texto transformado según la personalidad
        """
        personality = self.get_active_personality()
        if not personality:
            return response

        # Aplicar estilo de verbosidad
        response = self._apply_verbosity(response, personality)
        
        # Aplicar tono de voz
        response = self._apply_tone(response, personality)
        
        # Aplicar patrones de respuesta específicos del contexto
        response = self._apply_context_patterns(response)
        
        # Eliminar cualquier código de herramienta que pueda estar en la respuesta
        if "```tool_code" in response:
            response = response.split("```tool_code")[0].strip()
        
        return response

    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Genera un resumen detallado de la conversación.
        
        Returns:
            Diccionario con información de la conversación
        """
        return {
            "topics": self._extract_topics(),
            "sentiment": self._detect_sentiment(),
            "context_length": len(self.conversation_context)
        }
