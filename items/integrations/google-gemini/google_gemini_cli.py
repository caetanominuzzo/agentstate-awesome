#!/usr/bin/env python3
"""Google Gemini CLI for chatting with Gemini models and listing available models."""
import argparse
import json
import os
import sys

import google.generativeai as genai


class GeminiClient:
    """Client for Google Gemini API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "GEMINI_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        genai.configure(api_key=self.api_key)
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

    def chat(self, message):
        """Send a message to a Gemini model."""
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(message)
            return {
                "model": self.model_name,
                "text": response.text,
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": part.text} for part in c.content.parts],
                            "role": c.content.role,
                        },
                        "finish_reason": str(c.finish_reason),
                    }
                    for c in response.candidates
                ],
                "usage_metadata": {
                    "prompt_token_count": getattr(
                        response.usage_metadata, "prompt_token_count", None
                    ),
                    "candidates_token_count": getattr(
                        response.usage_metadata, "candidates_token_count", None
                    ),
                    "total_token_count": getattr(
                        response.usage_metadata, "total_token_count", None
                    ),
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def list_models(self):
        """List available Gemini models."""
        try:
            models = genai.list_models()
            return {
                "models": [
                    {
                        "name": m.name,
                        "display_name": m.display_name,
                        "description": m.description,
                        "supported_generation_methods": m.supported_generation_methods,
                    }
                    for m in models
                ]
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Google Gemini CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    chat_parser = subparsers.add_parser("chat", help="Send a message to Gemini")
    chat_parser.add_argument("--message", required=True, help="Message to send")

    subparsers.add_parser("list-models", help="List available models")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GeminiClient()

    if args.command == "chat":
        result = client.chat(args.message)
    elif args.command == "list-models":
        result = client.list_models()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
