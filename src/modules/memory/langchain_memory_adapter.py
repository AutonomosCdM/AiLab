from langchain.memory import ConversationBufferMemory

class LangChainMemoryAdapter:
    def __init__(self):
        """
        Initializes the LangChainMemoryAdapter with different LangChain memory types.
        """
        self.buffer_memory = ConversationBufferMemory(memory_key="history", input_key="input")

    def save_context(self, input_str, output_str, memory_instance):
        """
        Saves conversation context to the provided LangChain memory instance.
        """
        memory_instance.save_context({"input": input_str}, {"output": output_str})

    def load_memory_variables(self, memory_instance):
        """
        Loads memory variables from the provided LangChain memory instance.
        """
        return memory_instance.load_memory_variables({})

    def clear(self, memory_instance):
        """
        Clears the provided LangChain memory instance.
        """
        memory_instance.clear()

    def get_buffer_memory(self):
        """
        Returns the ConversationBufferMemory instance.
        """
        return self.buffer_memory
