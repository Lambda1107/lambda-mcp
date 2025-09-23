"""
Lambda MCP - A Python MCP server for Elasticsearch queries via Kibana.

This package provides a FastMCP-based server for querying Elasticsearch
clusters through Kibana's proxy API.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from lambda_mcp import main, query_elasticsearch_via_kibana

__all__ = ["main", "query_elasticsearch_via_kibana"]