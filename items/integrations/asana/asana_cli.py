#!/usr/bin/env python3
"""Asana CLI for managing workspaces, projects, and tasks."""
import argparse
import json
import os
import sys
import requests


class AsanaClient:
    """Client for Asana API interactions."""

    def __init__(self):
        self.token = os.environ.get("ASANA_ACCESS_TOKEN", "")
        if not self.token:
            print(
                '{"error": "ASANA_ACCESS_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_workspaces(self):
        """List all accessible workspaces."""
        try:
            response = requests.get(
                f"{self.base_url}/workspaces",
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

    def list_projects(self, workspace):
        """List projects in a workspace."""
        try:
            response = requests.get(
                f"{self.base_url}/projects",
                headers=self.headers,
                params={"workspace": workspace},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_task(self, project, name, notes=""):
        """Create a new task in a project."""
        payload = {
            "data": {
                "name": name,
                "notes": notes,
                "projects": [project],
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/tasks",
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

    def get_task(self, task_id):
        """Get details of a specific task."""
        try:
            response = requests.get(
                f"{self.base_url}/tasks/{task_id}",
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

    def update_task(self, task_id, completed=None):
        """Update a task's completion status."""
        payload = {"data": {}}
        if completed is not None:
            payload["data"]["completed"] = completed

        try:
            response = requests.put(
                f"{self.base_url}/tasks/{task_id}",
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
    parser = argparse.ArgumentParser(description="Asana CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-workspaces", help="List workspaces")

    proj_parser = subparsers.add_parser("list-projects", help="List projects")
    proj_parser.add_argument("--workspace", required=True, help="Workspace GID")

    create_parser = subparsers.add_parser("create-task", help="Create a task")
    create_parser.add_argument("--project", required=True, help="Project GID")
    create_parser.add_argument("--name", required=True, help="Task name")
    create_parser.add_argument("--notes", default="", help="Task notes")

    get_parser = subparsers.add_parser("get-task", help="Get task details")
    get_parser.add_argument("--task-id", required=True, help="Task GID")

    update_parser = subparsers.add_parser("update-task", help="Update a task")
    update_parser.add_argument("--task-id", required=True, help="Task GID")
    update_parser.add_argument(
        "--completed",
        required=True,
        choices=["true", "false"],
        help="Mark task completed or not",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = AsanaClient()

    if args.command == "list-workspaces":
        result = client.list_workspaces()
    elif args.command == "list-projects":
        result = client.list_projects(args.workspace)
    elif args.command == "create-task":
        result = client.create_task(args.project, args.name, args.notes)
    elif args.command == "get-task":
        result = client.get_task(args.task_id)
    elif args.command == "update-task":
        result = client.update_task(args.task_id, args.completed == "true")

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
