#!/usr/bin/env python3
"""Slack CLI for sending messages, listing channels, and posting block messages."""
import argparse
import json
import os
import sys
import requests


class SlackClient:
    """Client for Slack Web API interactions."""

    def __init__(self):
        self.token = os.environ.get("SLACK_BOT_TOKEN", "")
        if not self.token:
            print(
                '{"error": "SLACK_BOT_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def send_message(self, channel, text):
        """Send a text message to a Slack channel."""
        try:
            response = requests.post(
                f"{self.base_url}/chat.postMessage",
                headers=self.headers,
                json={"channel": channel, "text": text},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                return {"error": data.get("error", "Unknown Slack API error")}
            return data
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_channels(self):
        """List public channels in the workspace."""
        try:
            response = requests.get(
                f"{self.base_url}/conversations.list",
                headers=self.headers,
                params={"types": "public_channel", "limit": 200},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                return {"error": data.get("error", "Unknown Slack API error")}
            return data
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def post_blocks(self, channel, blocks_json):
        """Post a rich block message to a Slack channel."""
        try:
            blocks = json.loads(blocks_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid blocks JSON: {e}"}

        try:
            response = requests.post(
                f"{self.base_url}/chat.postMessage",
                headers=self.headers,
                json={"channel": channel, "blocks": blocks},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                return {"error": data.get("error", "Unknown Slack API error")}
            return data
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Slack CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send-message", help="Send a text message")
    send_parser.add_argument("--channel", required=True, help="Channel ID or name")
    send_parser.add_argument("--text", required=True, help="Message text")

    subparsers.add_parser("list-channels", help="List public channels")

    blocks_parser = subparsers.add_parser("post-blocks", help="Post a block message")
    blocks_parser.add_argument("--channel", required=True, help="Channel ID or name")
    blocks_parser.add_argument(
        "--blocks-json", required=True, help="JSON string of Slack blocks"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SlackClient()

    if args.command == "send-message":
        result = client.send_message(args.channel, args.text)
    elif args.command == "list-channels":
        result = client.list_channels()
    elif args.command == "post-blocks":
        result = client.post_blocks(args.channel, args.blocks_json)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
