#!/usr/bin/env python3
"""Elasticsearch CLI for searching, indexing, and managing indices and documents."""
import argparse
import json
import os
import sys

try:
    from elasticsearch import Elasticsearch, ElasticsearchException
except ImportError:
    print(
        '{"error": "elasticsearch package required. Install with: pip install elasticsearch>=8.10.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class ElasticsearchClient:
    """Client for Elasticsearch interactions."""

    def __init__(self):
        self.url = os.environ.get("ELASTICSEARCH_URL", "")
        if not self.url:
            print(
                '{"error": "ELASTICSEARCH_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        api_key = os.environ.get("ELASTICSEARCH_API_KEY", "")
        kwargs = {"hosts": [self.url], "request_timeout": 30}
        if api_key:
            kwargs["api_key"] = api_key
        try:
            self.client = Elasticsearch(**kwargs)
        except Exception as e:
            print(
                json.dumps({"error": f"Failed to connect to Elasticsearch: {str(e)}"}),
                file=sys.stderr,
            )
            sys.exit(1)

    def search(self, index, query_json):
        """Search an index with a query."""
        try:
            query = json.loads(query_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --query-json: {str(e)}"}

        try:
            result = self.client.search(index=index, body=query)
            return {
                "hits": result["hits"]["total"],
                "documents": [hit["_source"] for hit in result["hits"]["hits"]],
                "max_score": result["hits"]["max_score"],
            }
        except ElasticsearchException as e:
            return {"error": str(e)}

    def list_indices(self):
        """List all indices."""
        try:
            indices = self.client.cat.indices(format="json")
            return {"indices": indices}
        except ElasticsearchException as e:
            return {"error": str(e)}

    def get_document(self, index, doc_id):
        """Get a document by ID."""
        try:
            result = self.client.get(index=index, id=doc_id)
            return {
                "index": result["_index"],
                "id": result["_id"],
                "source": result["_source"],
                "version": result["_version"],
            }
        except ElasticsearchException as e:
            return {"error": str(e)}

    def index_document(self, index, doc_id, body_json):
        """Index (create/update) a document."""
        try:
            body = json.loads(body_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --body-json: {str(e)}"}

        try:
            result = self.client.index(index=index, id=doc_id, body=body)
            return {
                "result": result["result"],
                "index": result["_index"],
                "id": result["_id"],
                "version": result["_version"],
            }
        except ElasticsearchException as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Elasticsearch CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    search_parser = subparsers.add_parser("search", help="Search an index")
    search_parser.add_argument("--index", required=True, help="Index name")
    search_parser.add_argument(
        "--query-json", required=True, help="Search query as JSON string"
    )

    subparsers.add_parser("list-indices", help="List all indices")

    get_parser = subparsers.add_parser("get-document", help="Get a document by ID")
    get_parser.add_argument("--index", required=True, help="Index name")
    get_parser.add_argument("--id", required=True, help="Document ID")

    index_parser = subparsers.add_parser(
        "index-document", help="Index a document"
    )
    index_parser.add_argument("--index", required=True, help="Index name")
    index_parser.add_argument("--id", required=True, help="Document ID")
    index_parser.add_argument(
        "--body-json", required=True, help="Document body as JSON string"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = ElasticsearchClient()

    if args.command == "search":
        result = client.search(args.index, args.query_json)
    elif args.command == "list-indices":
        result = client.list_indices()
    elif args.command == "get-document":
        result = client.get_document(args.index, args.id)
    elif args.command == "index-document":
        result = client.index_document(args.index, args.id, args.body_json)

    print(json.dumps(result, indent=2, default=str))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
