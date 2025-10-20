"""
Elasticsearch tool for querying via Kibana proxy.
"""
import requests
import json
import jq
from typing import Annotated
from lib.response_utils import handle_large_response


def login(session, base_url, username, password):
    """Login to Kibana using Basic Auth."""
    # Use Basic Auth instead of POST login for this Kibana version
    session.auth = (username, password)
    # Test the auth by making a simple request to verify credentials
    test_url = base_url + '/api/status'
    response = session.get(test_url)
    response.raise_for_status()
    return True


def query_es(session, base_url, path, query_json):
    """Query Elasticsearch via Kibana proxy."""
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


def query_elasticsearch_via_kibana(
    base_url: Annotated[str, "Kibana base URL (e.g., https://kibana.example.com)"],
    username: Annotated[str, "Username for Kibana authentication, if no auth, use empty string"],
    password: Annotated[str, "Password for Kibana authentication, if no auth, use empty string"],
    path: Annotated[str, "Elasticsearch query path (e.g., index/_search)"],
    jq_query: Annotated[str, "jq query to filter the result, if no filter, use empty string. You must use filter when the result is long. Example: .[] | select(.index | contains(\"myindex\"))"] = "",
    query: Annotated[str, "JSON query body as string"] = "{}"
) -> str:
    """
    Query Elasticsearch via Kibana proxy.

    Returns:
        The query result as a JSON string, or a JSON object with file info if result is too large

    Example:
        query_elasticsearch_via_kibana(
            base_url="http://kibana.example.io",
            username="user_name",
            password="passwd",
            path="_cat/indices",
            jq_query=".[] | select(.index | contains(\"myindex\"))",
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
            
        # Apply jq filter if provided
        if jq_query:
            try:
                compiled_jq = jq.compile(jq_query)
                filtered_result = compiled_jq.input(result).all()
                result = filtered_result
            except Exception as e:
                raise ValueError(f"Invalid jq query: {e}")
            
        # Handle large response using common utility
        return handle_large_response(result)
            
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request error: {e}")

def register_elasticsearch_tool(mcp):
    """Register Elasticsearch tool with MCP server."""
    mcp.tool(query_elasticsearch_via_kibana)


