"""
Data Explorer client for querying databases through Data Service API.
"""
import time
import hmac
import hashlib
import requests
import uuid




class DataExplorer:
    """Client for querying databases through Data Service API."""
    ENDPOINT_QUERY = "/query"
    ENDPOINT_EXPLORE = "/explore_db"

    def __init__(self, secret: str, module_name: str, base_url: str):
        """
        Initialize DataExplorer client.
        
        Args:
            secret: Secret key for HMAC authentication
            module_name: Module name for the API request
            base_url: Base URL of the Data Service API
        """
        self.secret = secret
        self.module_name = module_name
        self.base_url = base_url

    def _generate_auth_headers(self) -> dict:
        """
        Generate authentication headers for API requests.
        
        Returns:
            Dictionary containing authentication headers
        """
        # Generate timestamp (milliseconds)
        timestamp = str(int(time.time() * 1000))
        
        # Generate HMAC-SHA256 hash as api-token
        hash_obj = hmac.new(
            self.secret.encode('utf-8'),
            timestamp.encode('utf-8'),
            hashlib.sha256
        )
        token = hash_obj.hexdigest()
        
        # Generate trace-id
        trace_id = str(uuid.uuid4())
        
        # Return headers
        return {
            "content-type": "application/json",
            "module-name": self.module_name,
            "timestamp": timestamp,
            "api-token": token,
            "trace-id": trace_id
        }

    def query_db(self, dbname: str, sql: str) -> list:
        """
        Execute SQL query on specified database.
        
        Args:
            dbname: Database name to query
            sql: SQL query string
            
        Returns:
            List of query results (dict records). Each record is a dictionary where keys are column names
            and values are the corresponding column values.
            
            Example return value:
            [
                {"id": 1, "name": "Alice", "age": 25},
                {"id": 2, "name": "Bob", "age": 30}
            ]
            
        Raises:
            Exception: If query fails or returns error
        """
        # Format SQL (normalize whitespace and quotes)
        sql = sql.replace('\n', ' ').replace('"', '%22').replace('\t', ' ').strip()
        
        # Build URL
        url = f"{self.base_url.rstrip('/')}{self.ENDPOINT_QUERY}/{dbname}"
        
        # Get authentication headers
        headers = self._generate_auth_headers()
        
        # Set request body
        payload = {
            "sql": sql
        }
        
        # Send POST request
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                raise Exception(
                    f"HTTP error: {response.status_code}, msg: {response.text}"
                )
            
            resp_json = response.json()
            if resp_json.get("code") != 0:
                raise Exception(
                    f"Query error: {resp_json.get('msg', 'Unknown error')}"
                )
            
            return resp_json.get("data", [])
            
        except Exception as e:
            raise Exception(f"Error occurred: {str(e)}")

    def explore_db(self) -> list:
        """
        Get list of all available databases.
        
        Returns:
            List of available database names as strings.
            
            Example return value:
            [
                "chatbot_api_db_sg",
                "chatbot_admin_db_sg",
                "inhouse_account_db",
                "presto_adhoc"
            ]
            
        Raises:
            Exception: If request fails or returns error
        """
        # Build URL
        url = f"{self.base_url.rstrip('/')}{self.ENDPOINT_EXPLORE}"
        
        # Get authentication headers
        headers = self._generate_auth_headers()
        
        # Send GET request
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(
                    f"HTTP error: {response.status_code}, msg: {response.text}"
                )
            
            resp_json = response.json()
            if resp_json.get("code") != 0:
                raise Exception(
                    f"Explore error: {resp_json.get('msg', 'Unknown error')}"
                )
            
            return resp_json.get("data", [])
            
        except Exception as e:
            raise Exception(f"Error occurred: {str(e)}")
