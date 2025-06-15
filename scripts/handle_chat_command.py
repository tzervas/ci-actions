"""
handle_chat_command.py

A simple script to handle chat commands for triggering GitHub Actions workflows via Slack.

Summary:
    This script listens for a specific chat command ("/start-build") and, when received, triggers a GitHub Actions workflow using the GitHub CLI. It then posts a confirmation message to a designated Slack channel. If an unknown command is received, it notifies the channel accordingly.

Inputs:
    - Command-line argument: The chat command to process (e.g., "/start-build").
    - Environment variable: SLACK_BOT_TOKEN (required for Slack API authentication).

Outputs:
    - Posts a message to the "#ci" Slack channel indicating the result of the command.

Expected Schemas:
    - Command: A single string argument representing the chat command.

Why:
    This implementation provides a lightweight integration between Slack and GitHub Actions, enabling users to trigger CI workflows directly from Slack. The use of the GitHub CLI and Slack SDK ensures reliability and leverages existing tools for workflow automation and messaging.

Usage:
    python handle_chat_command.py <command>
"""
import os
import subprocess
import sys

from slack_sdk import WebClient


def handle_chat_command(command):
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    if command == "/start-build":
        subprocess.run(["gh", "workflow", "run", "ci.yml"], check=True)
        client.chat_postMessage(channel="#ci", text="Build started!")
    else:
        client.chat_postMessage(channel="#ci", text="Unknown command")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python handle_chat_command.py <command>")
        sys.exit(1)
    handle_chat_command(sys.argv[1])
