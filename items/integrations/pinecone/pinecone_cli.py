#!/usr/bin/env python3
"""Pinecone CLI for managing vector database indexes and vectors."""
import argparse
import json
import os
import sys

from pinecone import Pinecone


class PineconeClient:
    """Client for Pinecone API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("PINECONE_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "PINECONE_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.pc = Pinecone(api_key=self.api_key)

    def list_indexes(self):
        """List all indexes."""
        try:
            indexes = self.pc.list_indexes()
            return {
                "indexes": [
                    {
                        "name": idx.name,
                        "dimension": idx.dimension,
                        "metric": idx.metric,
                        "host": idx.host,
                        "status": {"ready": idx.status.ready},
                    }
                    for idx in indexes
                ]
            }
        except Exception as e:
            return {"error": str(e)}

    def describe_index(self, index_name):
        """Describe an index."""
        try:
            desc = self.pc.describe_index(index_name)
            return {
                "name": desc.name,
                "dimension": desc.dimension,
                "metric": desc.metric,
                "host": desc.host,
                "status": {"ready": desc.status.ready},
            }
        except Exception as e:
            return {"error": str(e)}

    def query(self, index_name, vector, top_k=10):
        """Query an index with a vector."""
        try:
            index = self.pc.Index(index_name)
            results = index.query(vector=vector, top_k=top_k, include_metadata=True)
            return {
                "matches": [
                    {
                        "id": m.id,
                        "score": m.score,
                        "metadata": m.metadata,
                    }
                    for m in results.matches
                ]
            }
        except Exception as e:
            return {"error": str(e)}

    def upsert(self, index_name, vectors):
        """Upsert vectors into an index."""
        try:
            index = self.pc.Index(index_name)
            result = index.upsert(vectors=vectors)
            return {"upserted_count": result.upserted_count}
        except Exception as e:
            return {"error": str(e)}

    def delete(self, index_name, ids):
        """Delete vectors by IDs."""
        try:
            index = self.pc.Index(index_name)
            index.delete(ids=ids)
            return {"success": True, "deleted_ids": ids}
        except Exception as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Pinecone CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-indexes", help="List all indexes")

    describe_parser = subparsers.add_parser("describe-index", help="Describe an index")
    describe_parser.add_argument("--index", required=True, help="Index name")

    query_parser = subparsers.add_parser("query", help="Query an index")
    query_parser.add_argument("--index", required=True, help="Index name")
    query_parser.add_argument(
        "--vector-json", required=True, help="JSON array of floats for the query vector"
    )
    query_parser.add_argument(
        "--top-k", type=int, default=10, help="Number of results to return"
    )

    upsert_parser = subparsers.add_parser("upsert", help="Upsert vectors")
    upsert_parser.add_argument("--index", required=True, help="Index name")
    upsert_parser.add_argument(
        "--vectors-json",
        required=True,
        help='JSON array of vectors (e.g., \'[{"id":"v1","values":[0.1,0.2]}]\')',
    )

    delete_parser = subparsers.add_parser("delete", help="Delete vectors by IDs")
    delete_parser.add_argument("--index", required=True, help="Index name")
    delete_parser.add_argument(
        "--ids-json", required=True, help='JSON array of IDs (e.g., \'["v1","v2"]\')'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = PineconeClient()

    if args.command == "list-indexes":
        result = client.list_indexes()
    elif args.command == "describe-index":
        result = client.describe_index(args.index)
    elif args.command == "query":
        vector = json.loads(args.vector_json)
        result = client.query(args.index, vector, args.top_k)
    elif args.command == "upsert":
        vectors = json.loads(args.vectors_json)
        result = client.upsert(args.index, vectors)
    elif args.command == "delete":
        ids = json.loads(args.ids_json)
        result = client.delete(args.index, ids)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
