#!/usr/bin/env python3
"""
Lambda MCP Server - Main Entry Point

A Model Context Protocol (MCP) server providing various development tools.
"""

from fastmcp import FastMCP
from tools.elasticsearch import register_elasticsearch_tool
from tools.data_explorer import register_data_explorer_tool


def main():
    """Main entry point for the lambda-mcp server."""
    # Create FastMCP server
    mcp = FastMCP("Lambda Development Tools")
    
    # Register all tools
    register_elasticsearch_tool(mcp)
    register_data_explorer_tool(mcp)
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
