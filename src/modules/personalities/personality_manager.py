import json
import os

class PersonalityManager:
    def __init__(self, personalities_dir="src/modules/personalities/", default_personality="lucius_fox"):
        self.personalities_dir = personalities_dir
        self.personalities = self._load_personalities(default_personality) # Load only the default personality
        self.active_personality_name = default_personality
        if self.active_personality_name not in self.personalities:
            self.active_personality_name = list(self.personalities.keys())[0] if self.personalities else None

    def _load_personalities(self, personality_name):
        personalities = {}
        filename = f"{personality_name}.json"
        filepath = os.path.join(self.personalities_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                try:
                    personality_data = json.load(f)
                    personalities[personality_name] = personality_data
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in {filename}")
        else:
            print(f"Personality file not found: {filepath}")
        return personalities

    def get_active_personality(self):
        return self.personalities.get(self.active_personality_name)

    def transform_response(self, response: str) -> str:
        personality = self.get_active_personality()
        if personality:
            # Apply verbosity and tone constraints
            verbosity = personality.get('verbosity', 'Concise')
            tone = personality.get('tone', 'sharp_wit')

            # If verbosity is set to ultra-concise, make response extremely short
            if verbosity == 'Ultra-concise':
                # Use memory-specific templates if available
                memory_templates = personality.get('memory_response_templates', {})
                if 'memory_query' in memory_templates and 'memoria' in response.lower():
                    response = memory_templates['memory_query'][0]
                elif 'memory_confirmation' in memory_templates and 'memoria' in response.lower():
                    response = memory_templates['memory_confirmation'][0]
                else:
                    # Fallback: extremely short response
                    sentences = response.split('.')
                    response = sentences[0].split(',')[0].strip() + '.'

            # Add sarcastic or witty phrases if tone is sharp
            if tone == 'sharp_wit':
                phrases = personality.get('phrases', [])
                if phrases:
                    # Occasionally add a sarcastic phrase at the end
                    import random
                    if random.random() < 0.3:  # 30% chance
                        response += " " + random.choice(phrases)

            return response
        return response
