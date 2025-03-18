from lucius_agent import LuciusAgent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def run_cli_test():
    lucius_agent = LuciusAgent()
    print("Lucius Personality Test CLI")
    print("--------------------------")

    # First turn
    user_input_1 = "Buenos dias"
    print(f"User: {user_input_1}")
    response_1 = lucius_agent.handle_message(user_input_1)
    print(f"Lucius: {response_1}")

    # Second turn - follow up question to test memory
    user_input_2 = "Tienes memoria?"
    print(f"User: {user_input_2}")
    response_2 = lucius_agent.handle_message(user_input_2)
    print(f"Lucius: {response_2}")


if __name__ == "__main__":
    run_cli_test()
