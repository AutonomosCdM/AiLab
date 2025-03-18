import os
import logging
from langchain_community.agent_toolkits import SlackToolkit
from slack_sdk import WebClient

class SlackManager:
    def __init__(self):
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        slack_app_token = os.environ.get("SLACK_APP_TOKEN")

        # Log warning instead of raising error
        if not slack_bot_token:
            logging.warning("SLACK_BOT_TOKEN is not set. Slack tools will be limited.")
            self.slack_tools = []
            return

        if not slack_app_token:
            logging.warning("SLACK_APP_TOKEN is not set. Slack tools will be limited.")
            self.slack_tools = []
            return

        try:
            self.slack_toolkit = SlackToolkit(
                slack_client=WebClient(token=slack_bot_token)
            )
            self.slack_tools = self.slack_toolkit.get_tools()
            print(f"Slack tools available in SlackManager: {[tool.name for tool in self.slack_tools]}")
        except Exception as e:
            logging.error(f"Failed to initialize Slack toolkit: {e}")
            self.slack_tools = []

    def get_tools(self):
        return self.slack_tools

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Executes the specified tool and returns the output."""
        for tool in self.slack_tools:
            if tool.name == tool_name:
                return tool.run(tool_input)
        return f"Tool '{tool_name}' not found."
