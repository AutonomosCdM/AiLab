from lucius_agent import LuciusAgent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

if __name__ == "__main__":
    lucius_agent = LuciusAgent()
    print("Lucius Personality Test CLI")
    print("--------------------------")
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = lucius_agent.handle_message(user_input)
        print(f"Lucius: {response}")
