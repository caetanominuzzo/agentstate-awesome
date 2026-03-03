#!/usr/bin/env python3
"""SendGrid CLI for sending emails via the SendGrid v3 API."""
import argparse
import json
import os
import sys
import requests


class SendGridClient:
    """Client for SendGrid API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("SENDGRID_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "SENDGRID_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.sendgrid.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send(self, to, from_email, subject, text=None, html=None):
        """Send an email via SendGrid."""
        if not text and not html:
            return {"error": "Either --text or --html is required"}

        content = []
        if text:
            content.append({"type": "text/plain", "value": text})
        if html:
            content.append({"type": "text/html", "value": html})

        payload = {
            "personalizations": [{"to": [{"email": to}]}],
            "from": {"email": from_email},
            "subject": subject,
            "content": content,
        }

        try:
            response = requests.post(
                f"{self.base_url}/mail/send",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Email sent successfully",
            }
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


def main():
    parser = argparse.ArgumentParser(description="SendGrid CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send", help="Send an email")
    send_parser.add_argument("--to", required=True, help="Recipient email address")
    send_parser.add_argument(
        "--from", dest="from_email", required=True, help="Sender email address"
    )
    send_parser.add_argument("--subject", required=True, help="Email subject")
    send_parser.add_argument("--text", help="Plain text body")
    send_parser.add_argument("--html", help="HTML body")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SendGridClient()

    if args.command == "send":
        result = client.send(
            args.to, args.from_email, args.subject,
            text=args.text, html=args.html,
        )

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
