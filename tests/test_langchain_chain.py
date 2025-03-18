import unittest
import os
from dotenv import load_dotenv
from lucius_agent import chain  # Assuming chain is defined in lucius_agent.py

load_dotenv()

class TestLangchainChainIntegration(unittest.TestCase):

    def test_chain_invoke_groq_api(self):
        # Use actual chain and Groq LLM, relying on environment variables
        groq_api_key = os.environ.get("GROQ_API_KEY")
        self.assertIsNotNone(groq_api_key, "GROQ_API_KEY environment variable not set")

        # Invoke the chain with a sample input
        try:
            response = chain.invoke({"input": "Tell me a joke"})
            self.assertIsNotNone(response.content, "Response content is None")
            self.assertIsInstance(response.content, str, "Response content is not a string")
            self.assertGreater(len(response.content), 0, "Response content is empty")
            print(f"Groq API Response: {response.content}") # Print response for manual inspection
        except Exception as e:
            self.fail(f"Chain invoke failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
