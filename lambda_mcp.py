#!/usr/bin/env python3

import requests
import json
import os
from fastmcp import FastMCP
from typing import Annotated
from tokenizers import Tokenizer

# Load tokenizer for accurate token counting
tokenizer = Tokenizer.from_pretrained("gpt2")

MAX_TOKEN_NUM = 20000
if os.environ.get("LAMBDA_MCP_MAX_TOKEN_NUM") is not None:
    MAX_TOKEN_NUM = int(os.environ["LAMBDA_MCP_MAX_TOKEN_NUM"])

def login(session, base_url, username, password):
    # Use Basic Auth instead of POST login for this Kibana version
    session.auth = (username, password)
    # Test the auth by making a simple request to verify credentials
    test_url = base_url + '/api/status'
    response = session.get(test_url)
    response.raise_for_status()
    return True

def query_es(session, base_url, path, query_json):
    url = base_url + '/api/console/proxy'
    params = {
        'method': 'GET',
        'path': path
    }
    # For _cat endpoints, don't send query body
    data = '' if path.startswith('_cat') or path.startswith('/_cat') else query_json
    headers = {'Content-Type': 'application/json', 'kbn-xsrf': 'true'} if data else {'kbn-xsrf': 'true'}
    response = session.post(url, params=params, data=data, headers=headers)
    response.raise_for_status()
    # Try to parse as JSON, fallback to text
    try:
        return response.json()
    except ValueError:
        return response.text

# Create FastMCP server
mcp = FastMCP("Some develop tools")

@mcp.tool
def query_elasticsearch_via_kibana(
    base_url: Annotated[str, "Kibana base URL (e.g., https://kibana.example.com)"],
    username: Annotated[str, "Username for Kibana authentication, if no auth, use empty string"],
    password: Annotated[str, "Password for Kibana authentication, if no auth, use empty string"],
    path: Annotated[str, "Elasticsearch query path (e.g., index/_search)"],
    query: Annotated[str, "JSON query body as string"] = "{}"
) -> str:
    """
    Query Elasticsearch via Kibana proxy.

    Returns:
        The query result as a JSON string

    Example:
        query_elasticsearch_via_kibana(
            base_url="http://kibana.example.io",
            username="user_name",
            password="passwd",
            path="_cat/indices",
            query="{}"
        )
    """
    try:

        # Validate JSON query
        json.loads(query)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in query: {e}")

    session = requests.Session()

    try:
        login(session, base_url, username, password)
        result = query_es(session, base_url, path, query)
        result_str = json.dumps(result)
        token_count = len(tokenizer.encode(result_str))
        if token_count > MAX_TOKEN_NUM:
            raise Exception(f"Result exceeds {MAX_TOKEN_NUM} tokens, got {token_count} tokens, please refine your query.")

        else:
            return result_str
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request error: {e}")

def main():
    """Main entry point for the lambda-mcp script."""
    mcp.run()

if __name__ == "__main__":
    main()
