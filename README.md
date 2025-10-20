# Lambda MCP

A Python MCP (Model Context Protocol) server providing various development tools for data querying and analysis.

## Description

Lambda MCP is a FastMCP-based server that provides multiple tools for developers:
- **Elasticsearch Querying**: Query Elasticsearch clusters through Kibana's proxy API
- **Data Explorer**: Execute SQL queries against databases through Data Service API

The server includes smart response handling with automatic token counting to manage large responses efficiently.

## Features

- Query Elasticsearch via Kibana proxy
- Query databases via Data Service API with HMAC authentication
- Support for Basic Authentication (Kibana) and HMAC-SHA256 (Data Service)
- Token counting with configurable limits
- Automatic file output for large responses
- JSON query validation and jq filtering support
- Error handling for network and authentication issues
- Modular architecture for easy extension

## Installation

### From source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lambda-mcp.git
cd lambda-mcp
```

2. Install the package:
```bash
pip install -e .
```

### Using pip

```bash
pip install lambda-mcp
```

## Usage

### As a standalone script

```bash
python lambda_mcp.py
```

### Using the installed command

```bash
lambda-mcp
```

### Environment Variables

- `LAMBDA_MCP_MAX_TOKEN_NUM`: Maximum number of tokens allowed in response before saving to file (default: 30000)

## Available Tools

### 1. query_elasticsearch_via_kibana

Query Elasticsearch via Kibana proxy with optional jq filtering.

**Parameters:**
- `base_url` (str): Kibana base URL (e.g., https://kibana.example.com)
- `username` (str): Username for Kibana authentication (use empty string if no auth required)
- `password` (str): Password for Kibana authentication (use empty string if no auth required)
- `path` (str): Elasticsearch query path (e.g., index/_search, _cat/indices)
- `jq_query` (str, optional): jq query to filter results (default: "")
- `query` (str, optional): JSON query body as string (default: "{}")

**Returns:**
- str: Query result as JSON string, or file info JSON if result is too large

**Example:**
```python
result = query_elasticsearch_via_kibana(
    base_url="http://kibana.example.com",
    username="your_username",
    password="your_password",
    path="_cat/indices",
    jq_query='.[] | select(.index | contains("myindex"))',
    query="{}"
)
```

### 2. query_data_explorer

Execute SQL queries on databases through Data Service API.

**Parameters:**
- `secret` (str): Secret key for HMAC authentication
- `module_name` (str): Module name for the API request
- `base_url` (str): Base URL of the Data Service API (e.g., https://data-service.example.com)
- `api_path` (str): API path for query endpoint (e.g., api/v1/service/query)
- `dbname` (str): Database name to query
- `sql` (str): SQL query string to execute

**Returns:**
- str: Query result as JSON string, or file info JSON if result is too large

**Example:**
```python
result = query_data_explorer(
    secret="your_secret_key",
    module_name="chatbot_admin",
    base_url="https://data-service.example.com",
    api_path="api/v1/service/query",
    dbname="my_database",
    sql="SELECT * FROM users WHERE created_at > '2024-01-01' LIMIT 100"
)
```

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for detailed information about the project architecture and how to extend it.

## Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Code formatting

```bash
black lambda_mcp.py lib/ tools/
isort lambda_mcp.py lib/ tools/
```

### Type checking

```bash
mypy lambda_mcp.py lib/ tools/
```

## Dependencies

- `requests>=2.25.0`: HTTP library for API calls
- `fastmcp>=0.1.0`: FastMCP framework for MCP servers
- `tokenizers>=0.13.0`: Token counting functionality
- `jq>=1.0.0`: JSON filtering

## Security Notes

- **No credentials are stored**: All authentication credentials (passwords, secrets, API keys) must be provided by the caller
- **No URLs are hardcoded**: All service endpoints must be provided at runtime
- **Temporary files**: Large responses are saved to temporary files which should be cleaned up after use


## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.