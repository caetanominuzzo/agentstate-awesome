#!/usr/bin/env python3
"""Generic Telegram notification tool via Bot API."""
import argparse
import json
import os
import sys
import requests


SEVERITY_EMOJI = {
    "INFO": "\u2139\ufe0f",
    "WARNING": "\u26a0\ufe0f",
    "CRITICAL": "\ud83d\udea8",
}


class TelegramNotifier:
    """Client for sending notifications via Telegram Bot API."""

    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            print(
                '{"error": "TELEGRAM_BOT_TOKEN environment variable not set"}',
                file=sys.stderr,
            )
            sys.exit(1)

        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not self.chat_id:
            print(
                '{"error": "TELEGRAM_CHAT_ID environment variable not set"}',
                file=sys.stderr,
            )
            sys.exit(1)

        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, text, parse_mode=None):
        """Send a plain text message to the configured chat.

        Args:
            text: Message text (up to 4096 characters).
            parse_mode: Optional parse mode - "HTML", "Markdown", or "MarkdownV2".

        Returns:
            dict with the API response or error.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": text,
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode

        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                return {
                    "success": True,
                    "message_id": data["result"]["message_id"],
                    "chat_id": self.chat_id,
                }
            return {"error": data.get("description", "Unknown Telegram API error")}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def send_alert(self, title, fields_dict, severity="INFO", extra_context=None):
        """Send a formatted alert message with structured fields.

        Args:
            title: Alert title.
            fields_dict: Dictionary of field_name -> field_value pairs.
            severity: One of "INFO", "WARNING", "CRITICAL".
            extra_context: Optional additional text appended at the end.

        Returns:
            dict with the API response or error.
        """
        severity = severity.upper()
        emoji = SEVERITY_EMOJI.get(severity, SEVERITY_EMOJI["INFO"])

        lines = [f"{emoji} <b>{severity}: {title}</b>", ""]

        for key, value in fields_dict.items():
            lines.append(f"<b>{key}:</b> {value}")

        if extra_context:
            lines.append("")
            lines.append(extra_context)

        message = "\n".join(lines)
        return self.send_message(message, parse_mode="HTML")

    def get_bot_info(self):
        """Verify bot connectivity by calling getMe.

        Returns:
            dict with bot information or error.
        """
        try:
            response = requests.get(
                f"{self.base_url}/getMe",
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                bot = data["result"]
                return {
                    "success": True,
                    "bot_id": bot["id"],
                    "bot_name": bot.get("first_name", ""),
                    "bot_username": bot.get("username", ""),
                }
            return {"error": data.get("description", "Unknown Telegram API error")}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Telegram Notification CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # send command
    send_parser = subparsers.add_parser("send", help="Send a plain text message")
    send_parser.add_argument("--text", required=True, help="Message text")
    send_parser.add_argument(
        "--parse-mode",
        choices=["HTML", "Markdown", "MarkdownV2"],
        default=None,
        help="Parse mode for formatting",
    )

    # alert command
    alert_parser = subparsers.add_parser("alert", help="Send a formatted alert")
    alert_parser.add_argument("--title", required=True, help="Alert title")
    alert_parser.add_argument(
        "--fields",
        required=True,
        help='JSON object of field_name:value pairs (e.g., \'{"CPU": "95%%", "Host": "prod-1"}\')',
    )
    alert_parser.add_argument(
        "--severity",
        choices=["INFO", "WARNING", "CRITICAL"],
        default="INFO",
        help="Alert severity level (default: INFO)",
    )
    alert_parser.add_argument(
        "--context", default=None, help="Additional context text"
    )

    # info command
    subparsers.add_parser("info", help="Get bot info to verify connectivity")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    notifier = TelegramNotifier()

    if args.command == "send":
        result = notifier.send_message(args.text, parse_mode=args.parse_mode)
    elif args.command == "alert":
        try:
            fields = json.loads(args.fields)
        except json.JSONDecodeError as e:
            print(
                json.dumps({"error": f"Invalid JSON for --fields: {e}"}), file=sys.stderr
            )
            sys.exit(1)
        result = notifier.send_alert(
            args.title, fields, severity=args.severity, extra_context=args.context
        )
    elif args.command == "info":
        result = notifier.get_bot_info()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
