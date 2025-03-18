import json
import os
import random
from typing import List, Dict, Any

class SimplePersonalityManager:
    """
    A simplified personality manager that focuses on the core functionality
    without the complexity of the original implementation.
    """
    
    def __init__(self, personalities_dir="src/modules/personalities/", default_personality_name="lucius_fox"):
        self.personalities_dir = personalities_dir
        self.personalities = self._load_personalities()
        self.active_personality_name = default_personality_name
        self.conversation_context = []
        self.max_context_length = 5
    
    def _load_personalities(self):
        """Load all personality JSON files from the personalities directory"""
        personalities = {}
        
        if not os.path.exists(self.personalities_dir):
            print(f"Personalities directory does not exist: {self.personalities_dir}")
            return self._create_default_personality()
        
        for filename in os.listdir(self.personalities_dir):
            if filename.endswith('.json'):
                personality_name = filename[:-5]
                filepath = os.path.join(self.personalities_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        personality_data = json.load(f)
                        personalities[personality_name] = personality_data
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
        
        if not personalities:
            print("No valid personalities found")
            default_personality = self._create_default_personality()
            personalities['default'] = default_personality['default']
        
        return personalities
    
    def _create_default_personality(self):
        """Create a default personality if none are found"""
        return {
            'default': {
                "name": "default",
                "description": "Default personality with a helpful and concise tone.",
                "traits": ["helpful", "professional", "concise"],
                "tone": "neutral",
                "verbosity": "Concise"
            }
        }
    
    def get_active_personality(self):
        """Get the currently active personality"""
        return self.personalities.get(self.active_personality_name)
    
    def set_active_personality(self, personality_name):
        """Set the active personality"""
        if personality_name in self.personalities:
            self.active_personality_name = personality_name
            return True
        return False
    
    def list_available_personalities(self):
        """List all available personalities"""
        return list(self.personalities.keys())
    
    def update_conversation_context(self, user_input: str, agent_response: str):
        """Update the conversation context with the latest interaction"""
        context_entry = {
            "user_input": user_input,
            "agent_response": agent_response
        }
        
        self.conversation_context.append(context_entry)
        
        if len(self.conversation_context) > self.max_context_length:
            self.conversation_context.pop(0)
    
    def transform_response(self, response: str) -> str:
        """
        Apply simple transformations to the response based on the active personality.
        This is a simplified version that focuses on keeping responses concise.
        """
        personality = self.get_active_personality()
        if not personality:
            return response
        
        # Apply verbosity setting
        verbosity = personality.get('verbosity', 'Concise')
        
        # Split into sentences
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        
        if not sentences:
            return response
        
        # Apply verbosity rules
        if verbosity == 'Ultra-concise':
            # Return only the first sentence
            return sentences[0] + '.'
        elif verbosity == 'Concise':
            # Return at most 2 sentences
            return '. '.join(sentences[:2]) + '.'
        
        # For other verbosity levels, return the original response
        return response
    
    def generate_dynamic_system_prompt(self, base_prompt: str) -> str:
        """
        Generate a simple system prompt with minimal dynamic elements.
        """
        personality = self.get_active_personality()
        
        # Add basic personality traits to the prompt
        traits = personality.get('traits', [])
        traits_str = ', '.join(traits) if traits else 'helpful, concise'
        
        dynamic_prompt = f"""{base_prompt}

Personality Traits: {traits_str}

Communication Guidelines:
- Keep responses concise and to the point
- Be direct and avoid unnecessary elaboration
- Focus on providing accurate and helpful information
"""
        return dynamic_prompt
