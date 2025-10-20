# Lambda MCP Project Structure

## Overview

Lambda MCP is a Model Context Protocol (MCP) server that provides various development tools for querying data sources like Elasticsearch and Data Service APIs.

## Directory Structure

```
lambda-mcp/
├── lambda_mcp.py              # Main entry point - registers and runs all tools
├── pyproject.toml             # Project configuration and dependencies
├── README.md                  # Project documentation
│
├── lib/                       # Shared library code
│   ├── __init__.py
│   ├── data_explorer_client.py   # DataExplorer client for Data Service API
│   └── response_utils.py         # Common utilities for handling responses
│
└── tools/                     # MCP tool implementations
    ├── __init__.py
    ├── data_explorer.py       # Data Explorer query tool
    └── elasticsearch.py       # Elasticsearch/Kibana query tool
```

## Module Descriptions

### Main Entry Point

#### `lambda_mcp.py`

- **Purpose**: Main entry point for the MCP server
- **Responsibilities**:
  - Create FastMCP server instance
  - Register all tools
  - Start the server
- **Design**: Keep this file minimal - only orchestration, no business logic

### Library Modules (`lib/`)

#### `lib/data_explorer_client.py`

- **Purpose**: Client implementation for Data Service API
- **Key Class**: `DataExplorer`
  - Handles HMAC-SHA256 authentication
  - Executes SQL queries against databases
  - Returns structured query results
- **Note**: Does not store any credentials or URLs - all provided by caller

#### `lib/response_utils.py`

- **Purpose**: Common utilities for handling tool responses
- **Key Function**: `handle_large_response(data, max_tokens)`
  - Automatically handles large responses
  - If data exceeds token limit, saves to temporary file
  - Returns either JSON string or file metadata
  - Configurable via `LAMBDA_MCP_MAX_TOKEN_NUM` environment variable (default: 30000)

### Tool Modules (`tools/`)

Each tool module follows this pattern:

1. Import necessary dependencies
2. Define helper functions (if needed)
3. Implement `register_*_tool(mcp)` function that registers the tool

#### `tools/data_explorer.py`

- **Tool Name**: `query_data_explorer`
- **Purpose**: Query databases through Data Service API
- **Parameters**:
  - `secret`: Secret key for HMAC authentication
  - `module_name`: Module name for API request
  - `base_url`: Data Service API base URL
  - `api_path`: API endpoint path
  - `dbname`: Target database name
  - `sql`: SQL query string
- **Returns**: Query results (JSON) or file info if too large
- **Security**: No credentials stored; all provided by caller

#### `tools/elasticsearch.py`

- **Tool Name**: `query_elasticsearch_via_kibana`
- **Purpose**: Query Elasticsearch via Kibana proxy
- **Parameters**:
  - `base_url`: Kibana base URL
  - `username`: Kibana username
  - `password`: Kibana password
  - `path`: Elasticsearch query path
  - `jq_query`: Optional jq filter for results
  - `query`: JSON query body
- **Returns**: Query results (JSON) or file info if too large
- **Security**: No credentials stored; all provided by caller

## Design Principles

1. **Separation of Concerns**

   - Main entry point only handles orchestration
   - Business logic in library modules
   - Tool definitions separate from implementation

2. **Reusability**

   - Common functionality in `lib/` modules
   - Tools can share library code
   - Response handling is centralized

3. **Security**

   - No hardcoded credentials
   - All sensitive data provided by caller
   - Credentials never logged or persisted

4. **Scalability**
   - Easy to add new tools: create file in `tools/`, register in `lambda_mcp.py`
   - Easy to add new library modules: create in `lib/`, import where needed
   - Token limit configurable via environment variable

## Adding New Tools

To add a new tool:

1. Create a new file in `tools/` directory (e.g., `tools/my_new_tool.py`)
2. Implement the tool logic:

   ```python
   from typing import Annotated
   from lib.response_utils import handle_large_response

   def register_my_new_tool(mcp):
       @mcp.tool
       def my_new_tool(
           param1: Annotated[str, "Description"],
           param2: Annotated[int, "Description"]
       ) -> str:
           """Tool documentation"""
           # Implementation
           result = do_something(param1, param2)
           return handle_large_response(result)
   ```

3. Register in `lambda_mcp.py`:

   ```python
   from tools.my_new_tool import register_my_new_tool

   def main():
       mcp = FastMCP("Lambda Development Tools")
       register_my_new_tool(mcp)
       mcp.run()
   ```

## Adding New Library Modules

To add shared functionality:

1. Create a new file in `lib/` directory (e.g., `lib/my_module.py`)
2. Implement classes/functions with proper documentation
3. Import and use in tools as needed

## Environment Variables

- `LAMBDA_MCP_MAX_TOKEN_NUM`: Maximum tokens before saving response to file (default: 30000)

## Dependencies

See `pyproject.toml` for full dependency list. Key dependencies:

- `fastmcp`: MCP server framework
- `requests`: HTTP client
- `tokenizers`: Token counting
- `jq`: JSON filtering

## Usage

Run the server:

```bash
python lambda_mcp.py
```

Or if installed as package:

```bash
lambda-mcp
```
