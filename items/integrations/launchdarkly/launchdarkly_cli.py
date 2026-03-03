#!/usr/bin/env python3
"""LaunchDarkly CLI for managing feature flags, environments, and toggles."""
import argparse
import json
import os
import sys
import requests


class LaunchDarklyClient:
    """Client for LaunchDarkly API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("LAUNCHDARKLY_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "LAUNCHDARKLY_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.default_project_key = os.environ.get(
            "LAUNCHDARKLY_PROJECT_KEY", "default"
        )
        self.base_url = "https://app.launchdarkly.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

    def list_flags(self, project_key=None):
        """List all feature flags in a project."""
        pk = project_key or self.default_project_key
        try:
            response = requests.get(
                f"{self.base_url}/flags/{pk}",
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

    def get_flag(self, flag_key, project_key=None):
        """Get a specific feature flag."""
        pk = project_key or self.default_project_key
        try:
            response = requests.get(
                f"{self.base_url}/flags/{pk}/{flag_key}",
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

    def toggle_flag(self, flag_key, environment, on, project_key=None):
        """Toggle a feature flag on or off in an environment."""
        pk = project_key or self.default_project_key
        try:
            payload = [
                {
                    "op": "replace",
                    "path": f"/environments/{environment}/on",
                    "value": on,
                }
            ]
            response = requests.patch(
                f"{self.base_url}/flags/{pk}/{flag_key}",
                headers={
                    **self.headers,
                    "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
                },
                json={"instructions": [{"kind": "turnFlagOn" if on else "turnFlagOff"}]},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_environments(self, project_key=None):
        """List environments in a project."""
        pk = project_key or self.default_project_key
        try:
            response = requests.get(
                f"{self.base_url}/projects/{pk}/environments",
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
    parser = argparse.ArgumentParser(description="LaunchDarkly CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    flags_parser = subparsers.add_parser("list-flags", help="List feature flags")
    flags_parser.add_argument("--project-key", help="Project key (default: default)")

    flag_parser = subparsers.add_parser("get-flag", help="Get a feature flag")
    flag_parser.add_argument("--project-key", help="Project key (default: default)")
    flag_parser.add_argument("--flag-key", required=True, help="Flag key")

    toggle_parser = subparsers.add_parser("toggle-flag", help="Toggle a feature flag")
    toggle_parser.add_argument("--project-key", help="Project key (default: default)")
    toggle_parser.add_argument("--flag-key", required=True, help="Flag key")
    toggle_parser.add_argument(
        "--environment", required=True, help="Environment key"
    )
    toggle_group = toggle_parser.add_mutually_exclusive_group(required=True)
    toggle_group.add_argument("--on", action="store_true", help="Turn flag on")
    toggle_group.add_argument("--off", action="store_true", help="Turn flag off")

    envs_parser = subparsers.add_parser(
        "list-environments", help="List environments"
    )
    envs_parser.add_argument("--project-key", help="Project key (default: default)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = LaunchDarklyClient()

    if args.command == "list-flags":
        result = client.list_flags(
            project_key=getattr(args, "project_key", None),
        )
    elif args.command == "get-flag":
        result = client.get_flag(
            args.flag_key,
            project_key=getattr(args, "project_key", None),
        )
    elif args.command == "toggle-flag":
        result = client.toggle_flag(
            args.flag_key,
            args.environment,
            on=args.on,
            project_key=getattr(args, "project_key", None),
        )
    elif args.command == "list-environments":
        result = client.list_environments(
            project_key=getattr(args, "project_key", None),
        )

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
