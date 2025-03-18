import json
import os
from src.modules.memory.langchain_memory_adapter import LangChainMemoryAdapter

class MemoryManager:
    def __init__(self):
        """
        Initializes the MemoryManager and sets up memory adapters.
        """
        self.memory_adapter = LangChainMemoryAdapter()
        self.memory_instances = {
            "buffer": self.memory_adapter.get_buffer_memory(), # Using ConversationBufferMemory
            # Add other memory types here later (e.g., summary, vectorstore)
        }
        self.active_memory_type = "buffer" # Default memory type

    def get_memory(self, memory_type="buffer"):
        """
        Retrieves a specific memory instance based on memory_type.
        Defaults to 'buffer' memory type.
        """
        if memory_type not in self.memory_instances:
            raise ValueError(f"Memory type '{memory_type}' not supported.")
        return self.memory_instances[memory_type]

    def save_context(self, input_str, output_str, memory_type="buffer"):
        """
        Saves conversation context to the specified memory_type.
        Defaults to 'buffer' memory type.
        """
        memory_instance = self.get_memory(memory_type)
        self.memory_adapter.save_context(input_str, output_str, memory_instance)

    def load_memory_variables(self, memory_type="buffer"):
        """
        Loads relevant memory variables for the specified memory_type.
        Defaults to 'buffer' memory type.
        """
        memory_instance = self.get_memory(memory_type)
        return self.memory_adapter.load_memory_variables(memory_instance)

    def clear_memory(self, memory_type="buffer"):
        """
        Clears the memory of a specific memory_type.
        Defaults to 'buffer' memory type.
        """
        memory_instance = self.get_memory(memory_type)
        self.memory_adapter.clear(memory_instance)

    def set_active_memory_type(self, memory_type):
        """
        Sets the active memory type.
        """
        if memory_type not in self.memory_instances:
            raise ValueError(f"Memory type '{memory_type}' not supported.")
        self.active_memory_type = memory_type
