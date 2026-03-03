#!/usr/bin/env python3
"""Manage Devin knowledge notes (breadcrumbs) via the Devin API."""
import argparse
import json
import os
import sys
import requests


class DevinKnowledgeManager:
    """Client for managing Devin knowledge notes."""

    def __init__(self):
        self.api_token = os.environ.get("DEVIN_API")
        if not self.api_token:
            print(
                '{"error": "DEVIN_API environment variable not set"}', file=sys.stderr
            )
            sys.exit(1)

        self.base_url = "https://api.devin.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def get_knowledge(self, knowledge_id):
        """Retrieve a knowledge note by ID.

        Args:
            knowledge_id: The ID of the knowledge note.

        Returns:
            dict with the knowledge note content or error.
        """
        try:
            response = requests.get(
                f"{self.base_url}/knowledge/{knowledge_id}",
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

    def update_knowledge(self, knowledge_id, content):
        """Update a knowledge note by ID.

        Args:
            knowledge_id: The ID of the knowledge note.
            content: New content for the note.

        Returns:
            dict with success status or error.
        """
        payload = {"content": content}

        try:
            response = requests.patch(
                f"{self.base_url}/knowledge/{knowledge_id}",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "knowledge_id": knowledge_id}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_knowledge(self, title, content, trigger_type="keyword", trigger=None):
        """Create a new knowledge note.

        Args:
            title: Title of the knowledge note.
            content: Content of the note.
            trigger_type: How the note is triggered ("keyword", "always", etc.).
            trigger: Trigger value (e.g., keyword string).

        Returns:
            dict with the created note or error.
        """
        payload = {
            "title": title,
            "content": content,
            "trigger_type": trigger_type,
        }
        if trigger:
            payload["trigger"] = trigger

        try:
            response = requests.post(
                f"{self.base_url}/knowledge",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_knowledge(self):
        """List all knowledge notes.

        Returns:
            dict with the list of notes or error.
        """
        try:
            response = requests.get(
                f"{self.base_url}/knowledge",
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

    def update_breadcrumbs(self, target_ids, content):
        """Update multiple knowledge notes (breadcrumbs) with the same content.

        Args:
            target_ids: List of knowledge note IDs to update.
            content: Content to set on each note.

        Returns:
            dict with results for each target.
        """
        results = {}
        for kid in target_ids:
            results[kid] = self.update_knowledge(kid, content)
        return {
            "breadcrumb_results": results,
            "total": len(target_ids),
            "success_count": sum(
                1 for r in results.values() if r.get("success")
            ),
        }


def main():
    parser = argparse.ArgumentParser(description="Devin Knowledge Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # list command
    subparsers.add_parser("list", help="List all knowledge notes")

    # get command
    get_parser = subparsers.add_parser("get", help="Get a knowledge note by ID")
    get_parser.add_argument("--id", required=True, help="Knowledge note ID")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a knowledge note")
    create_parser.add_argument("--title", required=True, help="Note title")
    create_parser.add_argument("--content", required=True, help="Note content")
    create_parser.add_argument(
        "--trigger-type",
        default="keyword",
        help="Trigger type (default: keyword)",
    )
    create_parser.add_argument("--trigger", default=None, help="Trigger value")

    # update command
    update_parser = subparsers.add_parser("update", help="Update a knowledge note")
    update_parser.add_argument("--id", required=True, help="Knowledge note ID")
    update_parser.add_argument("--content", required=True, help="New content")

    # breadcrumbs command
    bc_parser = subparsers.add_parser(
        "breadcrumbs", help="Update multiple knowledge notes with the same content"
    )
    bc_parser.add_argument(
        "--targets",
        required=True,
        help="Comma-separated list of knowledge note IDs",
    )
    bc_parser.add_argument(
        "--content", required=True, help="Content to set on each note"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = DevinKnowledgeManager()

    if args.command == "list":
        result = manager.list_knowledge()
    elif args.command == "get":
        result = manager.get_knowledge(args.id)
    elif args.command == "create":
        result = manager.create_knowledge(
            args.title, args.content, args.trigger_type, args.trigger
        )
    elif args.command == "update":
        result = manager.update_knowledge(args.id, args.content)
    elif args.command == "breadcrumbs":
        target_ids = [t.strip() for t in args.targets.split(",")]
        result = manager.update_breadcrumbs(target_ids, args.content)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
