#!/usr/bin/env python3
"""MongoDB CLI for querying and managing databases and collections."""
import argparse
import json
import os
import sys

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError:
    print(
        '{"error": "pymongo package required. Install with: pip install pymongo>=4.5.0"}',
        file=sys.stderr,
    )
    sys.exit(1)

from bson import json_util


class MongoDBClient:
    """Client for MongoDB interactions."""

    def __init__(self):
        self.uri = os.environ.get("MONGODB_URI", "")
        if not self.uri:
            print(
                '{"error": "MONGODB_URI environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=30000)
        except PyMongoError as e:
            print(
                json.dumps({"error": f"Failed to connect to MongoDB: {str(e)}"}),
                file=sys.stderr,
            )
            sys.exit(1)

    def list_databases(self):
        """List all databases."""
        try:
            databases = self.client.list_database_names()
            db_info = []
            for db_name in databases:
                stats = self.client[db_name].command("dbStats")
                db_info.append({
                    "name": db_name,
                    "size_bytes": stats.get("dataSize", 0),
                    "collections": stats.get("collections", 0),
                })
            return {"databases": db_info}
        except PyMongoError as e:
            return {"error": str(e)}

    def list_collections(self, database):
        """List collections in a database."""
        try:
            db = self.client[database]
            collections = db.list_collection_names()
            return {"database": database, "collections": collections}
        except PyMongoError as e:
            return {"error": str(e)}

    def find(self, database, collection, filter_json=None, limit=20):
        """Find documents in a collection."""
        try:
            db = self.client[database]
            coll = db[collection]
            query_filter = {}
            if filter_json:
                query_filter = json.loads(filter_json)
            cursor = coll.find(query_filter).limit(limit)
            documents = json.loads(json_util.dumps(list(cursor)))
            return {
                "database": database,
                "collection": collection,
                "documents": documents,
                "count": len(documents),
            }
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --filter-json: {str(e)}"}
        except PyMongoError as e:
            return {"error": str(e)}

    def count(self, database, collection, filter_json=None):
        """Count documents in a collection."""
        try:
            db = self.client[database]
            coll = db[collection]
            query_filter = {}
            if filter_json:
                query_filter = json.loads(filter_json)
            doc_count = coll.count_documents(query_filter)
            return {
                "database": database,
                "collection": collection,
                "count": doc_count,
            }
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --filter-json: {str(e)}"}
        except PyMongoError as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="MongoDB CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-databases", help="List databases")

    coll_parser = subparsers.add_parser(
        "list-collections", help="List collections in a database"
    )
    coll_parser.add_argument("--database", required=True, help="Database name")

    find_parser = subparsers.add_parser("find", help="Find documents")
    find_parser.add_argument("--database", required=True, help="Database name")
    find_parser.add_argument("--collection", required=True, help="Collection name")
    find_parser.add_argument(
        "--filter-json", help="Filter query as JSON string"
    )
    find_parser.add_argument(
        "--limit", type=int, default=20, help="Max documents (default: 20)"
    )

    count_parser = subparsers.add_parser("count", help="Count documents")
    count_parser.add_argument("--database", required=True, help="Database name")
    count_parser.add_argument("--collection", required=True, help="Collection name")
    count_parser.add_argument(
        "--filter-json", help="Filter query as JSON string"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = MongoDBClient()

    if args.command == "list-databases":
        result = client.list_databases()
    elif args.command == "list-collections":
        result = client.list_collections(args.database)
    elif args.command == "find":
        result = client.find(
            args.database, args.collection, args.filter_json, args.limit
        )
    elif args.command == "count":
        result = client.count(args.database, args.collection, args.filter_json)

    print(json.dumps(result, indent=2, default=str))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
