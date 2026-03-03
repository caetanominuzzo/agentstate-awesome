#!/usr/bin/env python3
"""Microsoft Teams CLI for sending messages and adaptive cards via webhooks."""
import argparse
import json
import os
import sys
import requests


class TeamsClient:
    """Client for Microsoft Teams webhook interactions."""

    def __init__(self):
        self.webhook_url = os.environ.get("TEAMS_WEBHOOK_URL", "")
        if not self.webhook_url:
            print(
                '{"error": "TEAMS_WEBHOOK_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)

    def send(self, text):
        """Send a plain text message to Teams."""
        payload = {"text": text}

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "message": "Message sent to Teams"}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def send_card(self, title, text, color="0076D7"):
        """Send an adaptive card message to Teams."""
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": title,
            "sections": [
                {
                    "activityTitle": title,
                    "text": text,
                    "markdown": True,
                }
            ],
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "message": "Card sent to Teams", "title": title}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Microsoft Teams CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send", help="Send a text message")
    send_parser.add_argument("--text", required=True, help="Message text")

    card_parser = subparsers.add_parser("send-card", help="Send an adaptive card")
    card_parser.add_argument("--title", required=True, help="Card title")
    card_parser.add_argument("--text", required=True, help="Card body text")
    card_parser.add_argument(
        "--color", default="0076D7", help="Theme color hex (default: 0076D7)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = TeamsClient()

    if args.command == "send":
        result = client.send(args.text)
    elif args.command == "send-card":
        result = client.send_card(args.title, args.text, args.color)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
