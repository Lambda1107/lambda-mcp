"""
Data Explorer tool for querying databases through Data Service API.
"""
from typing import Annotated,Tuple
from lib.data_explorer_client import DataExplorer
from lib.response_utils import handle_large_response

EXPLORER_CONFIG_LIST = {
    "shopee_sg_test": ("https://data-service.test.sz.shopee.io/api/v1/service"),
    "shopee_sg_staging": ("https://data-service.staging.sz.shopee.io/api/v1/service"),
    "shopee_sg_uat": ("https://data-service.uat.sz.shopee.io/api/v1/service"),
    "shopee_sg_live": ("https://data-service.sz.shopee.io/api/v1/service"),
    "shopee_cn_live": ("https://cn.entrance.csinfra.shopee.io/dataservice"),
    "tutid_live": ("http://data-service.sz.tutid.io/api/v1/service"),
}

def get_auth_config_from_env(env_name: str) -> Tuple[str, str]:
    """Get Data Explorer auth config from environment name."""
    GENERAL_MODULE_NAME_KEY = "DATA_EXPLORER_MODULE_NAME"
    GENERAL_SECRET_KEY = "DATA_EXPLORER_SECRET"
    ENV_MODULE_NAME_KEY = f"{env_name.upper()}_DATA_EXPLORER_MODULE_NAME"
    ENV_SECRET_KEY = f"{env_name.upper()}_DATA_EXPLORER_SECRET"
    import os

    general_module_name = os.getenv(GENERAL_MODULE_NAME_KEY, "")
    general_secret = os.getenv(GENERAL_SECRET_KEY, "")
    env_module_name = os.getenv(ENV_MODULE_NAME_KEY, general_module_name)
    env_secret = os.getenv(ENV_SECRET_KEY, general_secret)

    if not env_module_name or not env_secret:
        if not general_module_name or not general_secret:
            raise ValueError("Data Explorer authentication configuration is missing.")
        else:
            return general_module_name, general_secret
    else:
        return env_module_name, env_secret

def query_data_explorer(
    env_name: Annotated[str, "Environment name (e.g., shopee_sg_test, shopee_sg_live, shopee_cn_live, tutid_live)"],
    dbname: Annotated[str, "Database name to query"],
    sql: Annotated[str, "SQL query string to execute"]
) -> str:
    """
    Query database through Data Service API.
        
    This tool allows you to execute SQL queries on databases through a Data Service API.
    It uses HMAC-SHA256 authentication and returns results as JSON.
    
    Authentication credentials (secret and module_name) are automatically retrieved from environment variables
    based on the env_name. The base URL is configured in EXPLORER_CONFIG_LIST.
        
    Returns:
        The query result as a JSON string, or a JSON object with file info if result is too large
        
    Example:
        query_data_explorer(
            env_name="shopee_sg_test",
            dbname="my_database",
            sql="SELECT * FROM users LIMIT 10"
        )
    """
    try:
        # Validate environment name
        if env_name not in EXPLORER_CONFIG_LIST:
            available_envs = ", ".join(EXPLORER_CONFIG_LIST.keys())
            raise ValueError(f"Invalid env_name '{env_name}'. Available environments: {available_envs}")
        
        # Get authentication config from environment variables
        module_name, secret = get_auth_config_from_env(env_name)
        
        # Get base URL from config
        base_url = EXPLORER_CONFIG_LIST[env_name]
        
        # Create DataExplorer client
        explorer = DataExplorer(
            secret=secret,
            module_name=module_name,
            base_url=base_url,
        )
            
        # Execute query
        result = explorer.query_db(dbname, sql)
            
        # Handle large response
        return handle_large_response(result)
            
    except Exception as e:
        raise RuntimeError(f"Query failed: {str(e)}")

def list_dbnames(
    env_name: Annotated[str, "Environment name (e.g., shopee_sg_test, shopee_sg_live, shopee_cn_live, tutid_live)"]
) -> str:
    """
    List all available databases in the specified environment.
    
    This tool retrieves a list of all database names accessible in the given environment.
    Authentication credentials are automatically retrieved from environment variables.
    
    Args:
        env_name: Environment name to query
        
    Returns:
        JSON string containing list of database names
        
    Example return:
        [
            "chatbot_api_db_sg",
            "chatbot_admin_db_sg",
            "inhouse_account_db"
        ]
        
    Example:
        list_dbnames(env_name="shopee_sg_test")
    """
    try:
        # Validate environment name
        if env_name not in EXPLORER_CONFIG_LIST:
            available_envs = ", ".join(EXPLORER_CONFIG_LIST.keys())
            raise ValueError(f"Invalid env_name '{env_name}'. Available environments: {available_envs}")
        
        # Get authentication config from environment variables
        module_name, secret = get_auth_config_from_env(env_name)
        
        # Get base URL from config
        base_url = EXPLORER_CONFIG_LIST[env_name]
        
        # Create DataExplorer client
        explorer = DataExplorer(
            secret=secret,
            module_name=module_name,
            base_url=base_url,
        )
            
        # Get database list
        result = explorer.explore_db()
            
        # Handle large response
        return handle_large_response(result)
            
    except Exception as e:
        raise RuntimeError(f"Failed to list databases: {str(e)}")

def list_tables(
    env_name: Annotated[str, "Environment name (e.g., shopee_sg_test, shopee_sg_live, shopee_cn_live, tutid_live)"],
    dbname: Annotated[str, "Database name to query tables from"]
) -> str:
    """
    List all tables in the specified database.
    
    This tool retrieves a list of all table names in the given database by executing a SHOW TABLES query.
    Authentication credentials are automatically retrieved from environment variables.
    
    Args:
        env_name: Environment name to query
        dbname: Database name to list tables from
        
    Returns:
        JSON string containing list of table information
        
    Example return:
        [
            {"Tables_in_database": "users"},
            {"Tables_in_database": "orders"},
            {"Tables_in_database": "products"}
        ]
        
    Example:
        list_tables(
            env_name="shopee_sg_test",
            dbname="chatbot_api_db_sg"
        )
    """
    try:
        # Validate environment name
        if env_name not in EXPLORER_CONFIG_LIST:
            available_envs = ", ".join(EXPLORER_CONFIG_LIST.keys())
            raise ValueError(f"Invalid env_name '{env_name}'. Available environments: {available_envs}")
        
        # Get authentication config from environment variables
        module_name, secret = get_auth_config_from_env(env_name)
        
        # Get base URL from config
        base_url = EXPLORER_CONFIG_LIST[env_name]
        
        # Create DataExplorer client
        explorer = DataExplorer(
            secret=secret,
            module_name=module_name,
            base_url=base_url,
        )
            
        # Execute SHOW TABLES query
        result = explorer.query_db(dbname, "SHOW TABLES")
            
        # Handle large response
        return handle_large_response(result)
            
    except Exception as e:
        raise RuntimeError(f"Failed to list tables: {str(e)}")

def get_data_explorer_env_names() -> str:
    """
    Get available Data Explorer environment names.
    
    Returns:
        JSON string containing list of available environment names and their URLs
    """
    import json
    
    env_info = {
        "environments": [
            {"name": env_name, "url": url}
            for env_name, url in EXPLORER_CONFIG_LIST.items()
        ]
    }
    return json.dumps(env_info, indent=2)

def register_data_explorer_tool(mcp):
    """Register Data Explorer tool and resources with MCP server."""
    
    mcp.tool(query_data_explorer)
    mcp.tool(list_dbnames)
    mcp.tool(list_tables)
    mcp.resource("data_explorer_env_names://")(get_data_explorer_env_names)
