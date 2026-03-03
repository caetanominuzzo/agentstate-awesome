#!/usr/bin/env python3
"""Resend CLI for sending emails and listing sent emails."""
import argparse
import json
import os
import sys
import requests


class ResendClient:
    """Client for Resend API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("RESEND_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "RESEND_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.resend.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send(self, to, from_email, subject, text=None, html=None):
        """Send an email via Resend."""
        if not text and not html:
            return {"error": "Either --text or --html is required"}

        payload = {
            "from": from_email,
            "to": [to],
            "subject": subject,
        }
        if text:
            payload["text"] = text
        if html:
            payload["html"] = html

        try:
            response = requests.post(
                f"{self.base_url}/emails",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_body = None
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_body = e.response.json()
                except ValueError:
                    error_body = e.response.text
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
                "details": error_body,
            }

    def list_emails(self):
        """List recently sent emails."""
        try:
            response = requests.get(
                f"{self.base_url}/emails",
                headers=self.headers,
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
    parser = argparse.ArgumentParser(description="Resend CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send", help="Send an email")
    send_parser.add_argument("--to", required=True, help="Recipient email address")
    send_parser.add_argument(
        "--from", dest="from_email", required=True, help="Sender email address"
    )
    send_parser.add_argument("--subject", required=True, help="Email subject")
    send_parser.add_argument("--text", help="Plain text body")
    send_parser.add_argument("--html", help="HTML body")

    subparsers.add_parser("list-emails", help="List recently sent emails")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = ResendClient()

    if args.command == "send":
        result = client.send(
            args.to, args.from_email, args.subject,
            text=args.text, html=args.html,
        )
    elif args.command == "list-emails":
        result = client.list_emails()

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
