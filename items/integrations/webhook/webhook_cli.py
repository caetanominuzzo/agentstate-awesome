#!/usr/bin/env python3
"""Webhook CLI for sending data to arbitrary webhook URLs with optional HMAC signing."""
import argparse
import hashlib
import hmac
import json
import os
import sys
import requests


class WebhookClient:
    """Client for generic webhook interactions."""

    def __init__(self):
        self.webhook_url = os.environ.get("WEBHOOK_URL", "")
        if not self.webhook_url:
            print(
                '{"error": "WEBHOOK_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.secret = os.environ.get("WEBHOOK_SECRET", "")

    def _build_headers(self, body_bytes):
        """Build request headers, optionally adding HMAC signature."""
        headers = {"Content-Type": "application/json"}
        if self.secret:
            signature = hmac.new(
                self.secret.encode("utf-8"),
                body_bytes,
                hashlib.sha256,
            ).hexdigest()
            headers["X-Signature-256"] = f"sha256={signature}"
        return headers

    def send(self, json_data=None, text=None):
        """Send data to the webhook URL."""
        if json_data:
            try:
                payload = json.loads(json_data)
            except json.JSONDecodeError as e:
                return {"error": f"Invalid JSON data: {e}"}
        elif text:
            payload = {"text": text}
        else:
            return {"error": "Either --json-data or --text is required"}

        body_bytes = json.dumps(payload).encode("utf-8")
        headers = self._build_headers(body_bytes)

        try:
            response = requests.post(
                self.webhook_url,
                data=body_bytes,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "body": response.text,
                }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def test(self):
        """Send a test ping to the webhook URL."""
        payload = {"event": "test", "message": "Webhook connectivity test"}
        body_bytes = json.dumps(payload).encode("utf-8")
        headers = self._build_headers(body_bytes)

        try:
            response = requests.post(
                self.webhook_url,
                data=body_bytes,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Webhook is reachable",
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Webhook CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    send_parser = subparsers.add_parser("send", help="Send data to webhook")
    send_parser.add_argument("--json-data", help="JSON string to send as body")
    send_parser.add_argument("--text", help="Plain text to send (wrapped in JSON)")

    subparsers.add_parser("test", help="Send a test ping to the webhook")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = WebhookClient()

    if args.command == "send":
        result = client.send(
            json_data=getattr(args, "json_data", None),
            text=getattr(args, "text", None),
        )
    elif args.command == "test":
        result = client.test()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
