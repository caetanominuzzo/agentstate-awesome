#!/usr/bin/env python3
"""Discord CLI for sending messages and embeds via webhooks."""
import argparse
import json
import os
import sys
import requests


class DiscordClient:
    """Client for Discord Webhook interactions."""

    def __init__(self):
        self.webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
        if not self.webhook_url:
            print(
                '{"error": "DISCORD_WEBHOOK_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)

    def send(self, text):
        """Send a text message via Discord webhook."""
        try:
            response = requests.post(
                self.webhook_url,
                json={"content": text},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            if response.status_code == 204:
                return {"success": True, "message": "Message sent"}
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def send_embed(self, title, description, color=None):
        """Send an embed message via Discord webhook."""
        embed = {"title": title, "description": description}
        if color is not None:
            embed["color"] = color

        try:
            response = requests.post(
                self.webhook_url,
                json={"embeds": [embed]},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            if response.status_code == 204:
                return {"success": True, "message": "Embed sent"}
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Discord CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send", help="Send a text message")
    send_parser.add_argument("--text", required=True, help="Message text")

    embed_parser = subparsers.add_parser("send-embed", help="Send an embed message")
    embed_parser.add_argument("--title", required=True, help="Embed title")
    embed_parser.add_argument(
        "--description", required=True, help="Embed description"
    )
    embed_parser.add_argument(
        "--color", type=int, default=None, help="Embed color as integer (e.g., 5814783)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = DiscordClient()

    if args.command == "send":
        result = client.send(args.text)
    elif args.command == "send-embed":
        result = client.send_embed(args.title, args.description, args.color)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
