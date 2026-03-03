#!/usr/bin/env python3
"""Doppler CLI for managing projects, configs, and secrets."""
import argparse
import json
import os
import sys
import requests


class DopplerClient:
    """Client for Doppler API interactions."""

    def __init__(self):
        self.token = os.environ.get("DOPPLER_TOKEN", "")
        if not self.token:
            print(
                '{"error": "DOPPLER_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.doppler.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_projects(self):
        """List all projects."""
        try:
            response = requests.get(
                f"{self.base_url}/projects",
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

    def list_configs(self, project):
        """List configs for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/configs",
                headers=self.headers,
                params={"project": project},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_secrets(self, project, config):
        """Get all secrets for a project config."""
        try:
            response = requests.get(
                f"{self.base_url}/configs/config/secrets",
                headers=self.headers,
                params={"project": project, "config": config},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_secret(self, project, config, name):
        """Get a single secret by name."""
        try:
            response = requests.get(
                f"{self.base_url}/configs/config/secret",
                headers=self.headers,
                params={"project": project, "config": config, "name": name},
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
    parser = argparse.ArgumentParser(description="Doppler CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-projects", help="List all projects")

    configs_parser = subparsers.add_parser("list-configs", help="List configs")
    configs_parser.add_argument("--project", required=True, help="Project name")

    secrets_parser = subparsers.add_parser("get-secrets", help="Get all secrets")
    secrets_parser.add_argument("--project", required=True, help="Project name")
    secrets_parser.add_argument("--config", required=True, help="Config name")

    secret_parser = subparsers.add_parser("get-secret", help="Get a single secret")
    secret_parser.add_argument("--project", required=True, help="Project name")
    secret_parser.add_argument("--config", required=True, help="Config name")
    secret_parser.add_argument("--name", required=True, help="Secret name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = DopplerClient()

    if args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "list-configs":
        result = client.list_configs(args.project)
    elif args.command == "get-secrets":
        result = client.get_secrets(args.project, args.config)
    elif args.command == "get-secret":
        result = client.get_secret(args.project, args.config, args.name)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
