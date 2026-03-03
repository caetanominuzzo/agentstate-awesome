#!/usr/bin/env python3
"""Render CLI for managing services, deployments, and environment variables."""
import argparse
import json
import os
import sys
import requests


class RenderClient:
    """Client for Render API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("RENDER_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "RENDER_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_services(self):
        """List all services."""
        try:
            response = requests.get(
                f"{self.base_url}/services",
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

    def get_service(self, service_id):
        """Get service details."""
        try:
            response = requests.get(
                f"{self.base_url}/services/{service_id}",
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

    def list_deploys(self, service_id):
        """List deploys for a service."""
        try:
            response = requests.get(
                f"{self.base_url}/services/{service_id}/deploys",
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

    def trigger_deploy(self, service_id):
        """Trigger a deploy for a service."""
        try:
            response = requests.post(
                f"{self.base_url}/services/{service_id}/deploys",
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

    def list_envs(self, service_id):
        """List environment variables for a service."""
        try:
            response = requests.get(
                f"{self.base_url}/services/{service_id}/env-vars",
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
    parser = argparse.ArgumentParser(description="Render CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-services", help="List all services")

    get_parser = subparsers.add_parser("get-service", help="Get service details")
    get_parser.add_argument("--service-id", required=True, help="Service ID")

    deploys_parser = subparsers.add_parser("list-deploys", help="List deploys")
    deploys_parser.add_argument("--service-id", required=True, help="Service ID")

    trigger_parser = subparsers.add_parser("trigger-deploy", help="Trigger a deploy")
    trigger_parser.add_argument("--service-id", required=True, help="Service ID")

    envs_parser = subparsers.add_parser(
        "list-envs", help="List environment variables"
    )
    envs_parser.add_argument("--service-id", required=True, help="Service ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = RenderClient()

    if args.command == "list-services":
        result = client.list_services()
    elif args.command == "get-service":
        result = client.get_service(args.service_id)
    elif args.command == "list-deploys":
        result = client.list_deploys(args.service_id)
    elif args.command == "trigger-deploy":
        result = client.trigger_deploy(args.service_id)
    elif args.command == "list-envs":
        result = client.list_envs(args.service_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
