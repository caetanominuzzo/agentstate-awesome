#!/usr/bin/env python3
"""ClickUp CLI for managing teams, spaces, and tasks."""
import argparse
import json
import os
import sys
import requests


class ClickUpClient:
    """Client for ClickUp API interactions."""

    def __init__(self):
        self.token = os.environ.get("CLICKUP_API_TOKEN", "")
        if not self.token:
            print(
                '{"error": "CLICKUP_API_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_teams(self):
        """List all accessible teams (workspaces)."""
        try:
            response = requests.get(
                f"{self.base_url}/team",
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

    def list_spaces(self, team_id):
        """List spaces in a team."""
        try:
            response = requests.get(
                f"{self.base_url}/team/{team_id}/space",
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

    def list_tasks(self, list_id):
        """List tasks in a list."""
        try:
            response = requests.get(
                f"{self.base_url}/list/{list_id}/task",
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

    def create_task(self, list_id, name, description=""):
        """Create a new task in a list."""
        payload = {"name": name, "description": description}

        try:
            response = requests.post(
                f"{self.base_url}/list/{list_id}/task",
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

    def update_task(self, task_id, status=None):
        """Update a task's status."""
        payload = {}
        if status is not None:
            payload["status"] = status

        try:
            response = requests.put(
                f"{self.base_url}/task/{task_id}",
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


def main():
    parser = argparse.ArgumentParser(description="ClickUp CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-teams", help="List teams")

    spaces_parser = subparsers.add_parser("list-spaces", help="List spaces in a team")
    spaces_parser.add_argument("--team-id", required=True, help="Team ID")

    tasks_parser = subparsers.add_parser("list-tasks", help="List tasks in a list")
    tasks_parser.add_argument("--list-id", required=True, help="List ID")

    create_parser = subparsers.add_parser("create-task", help="Create a task")
    create_parser.add_argument("--list-id", required=True, help="List ID")
    create_parser.add_argument("--name", required=True, help="Task name")
    create_parser.add_argument("--description", default="", help="Task description")

    update_parser = subparsers.add_parser("update-task", help="Update a task")
    update_parser.add_argument("--task-id", required=True, help="Task ID")
    update_parser.add_argument("--status", required=True, help="New task status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = ClickUpClient()

    if args.command == "list-teams":
        result = client.list_teams()
    elif args.command == "list-spaces":
        result = client.list_spaces(args.team_id)
    elif args.command == "list-tasks":
        result = client.list_tasks(args.list_id)
    elif args.command == "create-task":
        result = client.create_task(args.list_id, args.name, args.description)
    elif args.command == "update-task":
        result = client.update_task(args.task_id, args.status)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
