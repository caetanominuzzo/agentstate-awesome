#!/usr/bin/env python3
"""Mailgun CLI for sending emails and listing events."""
import argparse
import json
import os
import sys
import requests


class MailgunClient:
    """Client for Mailgun API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("MAILGUN_API_KEY", "")
        self.domain = os.environ.get("MAILGUN_DOMAIN", "")
        if not self.api_key or not self.domain:
            print(
                '{"error": "MAILGUN_API_KEY and MAILGUN_DOMAIN environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"https://api.mailgun.net/v3/{self.domain}"
        self.auth = ("api", self.api_key)

    def send(self, to, from_addr, subject, text=None, html=None):
        """Send an email."""
        if not text and not html:
            return {"error": "Either --text or --html is required"}

        data = {
            "from": from_addr,
            "to": [to],
            "subject": subject,
        }
        if text:
            data["text"] = text
        if html:
            data["html"] = html

        try:
            response = requests.post(
                f"{self.base_url}/messages",
                auth=self.auth,
                data=data,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_events(self, limit=100):
        """List recent email events."""
        try:
            response = requests.get(
                f"{self.base_url}/events",
                auth=self.auth,
                params={"limit": limit},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Mailgun CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send", help="Send an email")
    send_parser.add_argument("--to", required=True, help="Recipient email address")
    send_parser.add_argument("--from", dest="from_addr", required=True, help="Sender email address")
    send_parser.add_argument("--subject", required=True, help="Email subject")
    send_parser.add_argument("--text", help="Plain text body")
    send_parser.add_argument("--html", help="HTML body")

    events_parser = subparsers.add_parser("list-events", help="List recent events")
    events_parser.add_argument(
        "--limit", type=int, default=100, help="Max events (default: 100)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = MailgunClient()

    if args.command == "send":
        result = client.send(
            args.to, args.from_addr, args.subject, args.text, args.html
        )
    elif args.command == "list-events":
        result = client.list_events(args.limit)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
