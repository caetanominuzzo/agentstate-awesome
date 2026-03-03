#!/usr/bin/env python3
"""Twilio CLI for sending SMS and WhatsApp messages."""
import argparse
import json
import os
import sys
import requests


class TwilioClient:
    """Client for Twilio API interactions."""

    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER", "")
        if not self.account_sid or not self.auth_token or not self.from_number:
            print(
                '{"error": "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_FROM_NUMBER environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}"
        self.auth = (self.account_sid, self.auth_token)

    def send_sms(self, to, body):
        """Send an SMS message."""
        payload = {
            "From": self.from_number,
            "To": to,
            "Body": body,
        }

        try:
            response = requests.post(
                f"{self.base_url}/Messages.json",
                auth=self.auth,
                data=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def send_whatsapp(self, to, body):
        """Send a WhatsApp message."""
        payload = {
            "From": f"whatsapp:{self.from_number}",
            "To": f"whatsapp:{to}",
            "Body": body,
        }

        try:
            response = requests.post(
                f"{self.base_url}/Messages.json",
                auth=self.auth,
                data=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_messages(self, limit=20):
        """List recent messages."""
        try:
            response = requests.get(
                f"{self.base_url}/Messages.json",
                auth=self.auth,
                params={"PageSize": limit},
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
    parser = argparse.ArgumentParser(description="Twilio CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    sms_parser = subparsers.add_parser("send-sms", help="Send an SMS message")
    sms_parser.add_argument(
        "--to", required=True, help="Recipient phone number (e.g., +15559876543)"
    )
    sms_parser.add_argument("--body", required=True, help="Message body")

    wa_parser = subparsers.add_parser(
        "send-whatsapp", help="Send a WhatsApp message"
    )
    wa_parser.add_argument(
        "--to", required=True, help="Recipient phone number (e.g., +15559876543)"
    )
    wa_parser.add_argument("--body", required=True, help="Message body")

    list_parser = subparsers.add_parser("list-messages", help="List recent messages")
    list_parser.add_argument(
        "--limit", type=int, default=20, help="Max results (default: 20)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = TwilioClient()

    if args.command == "send-sms":
        result = client.send_sms(args.to, args.body)
    elif args.command == "send-whatsapp":
        result = client.send_whatsapp(args.to, args.body)
    elif args.command == "list-messages":
        result = client.list_messages(args.limit)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
