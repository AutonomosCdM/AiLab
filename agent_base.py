from abc import ABC, abstractmethod
from src.modules.memory.memory_manager import MemoryManager

class AgentBase(ABC):
    """
    Abstract base class for all agents in the system.
    Provides a common interface and shared functionality.
    """

    def __init__(self, name: str):
        """
        Initializes the AgentBase.

        Args:
            name (str): The name of the agent.
        """
        self.name = name
        self.memory_manager = MemoryManager() # Initialize MemoryManager
        self.context = {}  # Initialize context (can be expanded later)

    @abstractmethod
    def handle_message(self, user_message: str) -> str:
        """
        Abstract method to handle incoming user messages.
        Subclasses must implement this method to define agent-specific logic.

        Args:
            user_message (str): The message from the user.

        Returns:
            str: The agent's response to the user message.
        """
        pass

    def get_context(self) -> dict:
        """
        Returns the current context of the agent.

        Returns:
            dict: The agent's context.
        """
        return self.context

    def update_context(self, key: str, value: any):
        """
        Updates the agent's context with a new key-value pair.

        Args:
            key (str): The key to update in the context.
            value (any): The value to set for the key.
        """
        self.context[key] = value
