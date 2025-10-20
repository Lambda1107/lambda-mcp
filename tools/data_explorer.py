"""
Data Explorer tool for querying databases through Data Service API.
"""
from typing import Annotated
from lib.data_explorer_client import DataExplorer
from lib.response_utils import handle_large_response

def query_data_explorer(
    secret: Annotated[str, "Secret key for HMAC authentication"],
    module_name: Annotated[str, "Module name for the API request"],
    base_url: Annotated[str, "Base URL of the Data Service API (e.g., https://data-service.example.com)"],
    api_path: Annotated[str, "API path for query endpoint (e.g., api/v1/service/query)"],
    dbname: Annotated[str, "Database name to query"],
    sql: Annotated[str, "SQL query string to execute"]
) -> str:
    """
    Query database through Data Service API.
        
    This tool allows you to execute SQL queries on databases through a Data Service API.
    It uses HMAC-SHA256 authentication and returns results as JSON.
        
    Returns:
        The query result as a JSON string, or a JSON object with file info if result is too large
        
    Example:
        query_data_explorer(
            secret="your_secret_key",
            module_name="chatbot_admin",
            base_url="https://data-service.example.com",
            api_path="api/v1/service/query",
            dbname="my_database",
            sql="SELECT * FROM users LIMIT 10"
        )
    """
    try:
        # Create DataExplorer client
        explorer = DataExplorer(
            secret=secret,
            module_name=module_name,
            base_url=base_url,
            api_path=api_path
        )
            
        # Execute query
        result = explorer.query_db(dbname, sql)
            
        # Handle large response
        return handle_large_response(result)
            
    except Exception as e:
        raise RuntimeError(f"Query failed: {str(e)}")

def register_data_explorer_tool(mcp):
    """Register Data Explorer tool with MCP server."""
    
    mcp.tool(query_data_explorer)
