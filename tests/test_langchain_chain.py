import unittest
import os
from dotenv import load_dotenv
from src.llm.llm_service import LLMService
from src.config import Config

load_dotenv()

class TestLangchainChainIntegration(unittest.TestCase):

    def test_llm_service_invoke(self):
        # Use actual LLM service and Groq LLM, relying on environment variables
        groq_api_key = os.environ.get("GROQ_API_KEY")
        self.assertIsNotNone(groq_api_key, "GROQ_API_KEY environment variable not set")

        # Initialize LLM service
        llm_service = LLMService()

        # Invoke the LLM service with a sample input
        try:
            # Simulate tool descriptions for the test
            tool_descriptions = [
                {"name": "test_tool", "description": "A test tool for integration"}
            ]
            
            response = llm_service.generate_response("Tell me a joke", tool_descriptions)
            
            self.assertIsNotNone(response, "Response is None")
            self.assertIsInstance(response, str, "Response is not a string")
            self.assertGreater(len(response), 0, "Response is empty")
            print(f"Groq API Response: {response}") # Print response for manual inspection
        except Exception as e:
            self.fail(f"LLM service invoke failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
