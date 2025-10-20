#!/usr/bin/env python3
"""
Simple test script to verify tool functionality
"""

from lib.data_explorer_client import DataExplorer
from lib.response_utils import handle_large_response
import json


def test_data_explorer_client():
    """Test DataExplorer client initialization"""
    print("Testing DataExplorer client...")
    explorer = DataExplorer(
        secret="test_secret",
        module_name="test_module",
        base_url="https://test.example.com",
        api_path="api/v1/query"
    )
    assert explorer.secret == "test_secret"
    assert explorer.module_name == "test_module"
    assert explorer.base_url == "https://test.example.com"
    assert explorer.api_path == "api/v1/query"
    print("✅ DataExplorer client initialization works!")


def test_response_utils():
    """Test response utilities"""
    print("\nTesting response utilities...")
    
    # Test small response
    small_data = {"result": "success", "count": 10}
    result = handle_large_response(small_data)
    parsed = json.loads(result)
    assert parsed["result"] == "success"
    print("✅ Small response handling works!")
    
    # Test large response (create data that exceeds token limit)
    large_data = [{"id": i, "data": "x" * 1000} for i in range(1000)]
    result = handle_large_response(large_data, max_tokens=100)
    parsed = json.loads(result)
    assert parsed["type"] == "file"
    assert "path" in parsed
    print(f"✅ Large response saved to file: {parsed['path']}")
    print(f"   Reason: {parsed['reason']}")


def test_imports():
    """Test that all tools can be imported"""
    print("\nTesting tool imports...")
    from tools.data_explorer import register_data_explorer_tool
    from tools.elasticsearch import register_elasticsearch_tool
    print("✅ All tool modules import successfully!")


if __name__ == "__main__":
    print("=" * 60)
    print("Lambda MCP - Tool Testing")
    print("=" * 60)
    
    test_data_explorer_client()
    test_response_utils()
    test_imports()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)
