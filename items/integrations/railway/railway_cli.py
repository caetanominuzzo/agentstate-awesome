#!/usr/bin/env python3
"""Railway CLI for managing projects, services, and deployments."""
import argparse
import json
import os
import sys
import requests


class RailwayClient:
    """Client for Railway GraphQL API interactions."""

    def __init__(self):
        self.token = os.environ.get("RAILWAY_TOKEN", "")
        if not self.token:
            print(
                '{"error": "RAILWAY_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://backboard.railway.app/graphql/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _graphql(self, query, variables=None):
        """Execute a GraphQL query."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        try:
            response = requests.post(
                self.base_url,
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

    def list_projects(self):
        """List all projects."""
        query = """
        query {
          projects {
            edges {
              node {
                id
                name
                description
                createdAt
                updatedAt
              }
            }
          }
        }
        """
        return self._graphql(query)

    def get_project(self, project_id):
        """Get project details."""
        query = """
        query ($projectId: String!) {
          project(id: $projectId) {
            id
            name
            description
            createdAt
            updatedAt
            environments {
              edges {
                node {
                  id
                  name
                }
              }
            }
          }
        }
        """
        return self._graphql(query, {"projectId": project_id})

    def list_services(self, project_id):
        """List services in a project."""
        query = """
        query ($projectId: String!) {
          project(id: $projectId) {
            services {
              edges {
                node {
                  id
                  name
                  createdAt
                  updatedAt
                }
              }
            }
          }
        }
        """
        return self._graphql(query, {"projectId": project_id})

    def list_deployments(self, project_id):
        """List deployments for a project."""
        query = """
        query ($projectId: String!) {
          deployments(input: { projectId: $projectId }, first: 20) {
            edges {
              node {
                id
                status
                createdAt
                updatedAt
              }
            }
          }
        }
        """
        return self._graphql(query, {"projectId": project_id})

    def get_deployment(self, deployment_id):
        """Get deployment details."""
        query = """
        query ($deploymentId: String!) {
          deployment(id: $deploymentId) {
            id
            status
            createdAt
            updatedAt
            staticUrl
          }
        }
        """
        return self._graphql(query, {"deploymentId": deployment_id})


def main():
    parser = argparse.ArgumentParser(description="Railway CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-projects", help="List all projects")

    project_parser = subparsers.add_parser("get-project", help="Get project details")
    project_parser.add_argument("--project-id", required=True, help="Project ID")

    services_parser = subparsers.add_parser(
        "list-services", help="List services in a project"
    )
    services_parser.add_argument("--project-id", required=True, help="Project ID")

    deploys_parser = subparsers.add_parser(
        "list-deployments", help="List deployments"
    )
    deploys_parser.add_argument("--project-id", required=True, help="Project ID")

    deploy_parser = subparsers.add_parser(
        "get-deployment", help="Get deployment details"
    )
    deploy_parser.add_argument("--deployment-id", required=True, help="Deployment ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = RailwayClient()

    if args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "get-project":
        result = client.get_project(args.project_id)
    elif args.command == "list-services":
        result = client.list_services(args.project_id)
    elif args.command == "list-deployments":
        result = client.list_deployments(args.project_id)
    elif args.command == "get-deployment":
        result = client.get_deployment(args.deployment_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
