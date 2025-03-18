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
            return response # Return raw response without prefix
        return response
