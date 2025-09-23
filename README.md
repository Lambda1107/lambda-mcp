# Lambda MCP

A Python MCP (Model Context Protocol) server for querying Elasticsearch via Kibana proxy.

## Description

Lambda MCP is a FastMCP-based server that provides tools for querying Elasticsearch clusters through Kibana's proxy API. It supports authentication and includes token counting to manage response sizes.

## Features

- Query Elasticsearch via Kibana proxy
- Support for Basic Authentication
- Token counting with configurable limits
- JSON query validation
- Error handling for network and authentication issues

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

- `LAMBDA_MCP_MAX_TOKEN_NUM`: Maximum number of tokens allowed in response (default: 10000)

## API

### query_elasticsearch_via_kibana

Query Elasticsearch via Kibana proxy.

**Parameters:**
- `base_url` (str): Kibana base URL (e.g., https://kibana.example.com)
- `username` (str): Username for Kibana authentication (use empty string if no auth required)
- `password` (str): Password for Kibana authentication (use empty string if no auth required)
- `path` (str): Elasticsearch query path (e.g., index/_search)
- `query` (str, optional): JSON query body as string (default: "{}")

**Returns:**
- str: The query result as a JSON string

**Example:**
```python
result = query_elasticsearch_via_kibana(
    base_url="http://kibana.example.com",
    username="your_username",
    password="your_password",
    path="_cat/indices",
    query="{}"
)
```

## Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Code formatting

```bash
black lambda_mcp.py
isort lambda_mcp.py
```

### Type checking

```bash
mypy lambda_mcp.py
```

### Testing

```bash
pytest
```

## Dependencies

- `requests>=2.25.0`: HTTP library for API calls
- `fastmcp>=0.1.0`: FastMCP framework for MCP servers
- `tokenizers>=0.13.0`: Token counting functionality

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.