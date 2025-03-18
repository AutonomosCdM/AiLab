import os
from langchain_community.agent_toolkits import SlackToolkit
from slack_sdk import WebClient

class SlackManager:
    def __init__(self):
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        slack_app_token = os.environ.get("SLACK_APP_TOKEN")

        if not slack_bot_token:
            raise ValueError("SLACK_BOT_TOKEN is not set!")
        if not slack_app_token:
            raise ValueError("SLACK_APP_TOKEN is not set!")

        self.slack_toolkit = SlackToolkit(
            slack_client=WebClient(token=slack_bot_token)
        )
        self.slack_tools = self.slack_toolkit.get_tools()
        print(f"Slack tools available in SlackManager: {[tool.name for tool in self.slack_tools]}")

    def get_tools(self):
        return self.slack_tools

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Executes the specified tool and returns the output."""
        for tool in self.slack_tools:
            if tool.name == tool_name:
                return tool.run(tool_input)
        return f"Tool '{tool_name}' not found."
