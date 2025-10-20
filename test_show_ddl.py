#!/usr/bin/env python3
"""
Test script for show_table_ddl tool.
"""
import json
import os

# Set up environment variables for testing
os.environ["DATA_EXPLORER_MODULE_NAME"] = "chatbot_admin"
os.environ["DATA_EXPLORER_SECRET"] = "9b5f618608db30b792a97bc03563baa0"

from tools.data_explorer import show_table_ddl, list_tables


def main():
    """Test show_table_ddl functionality."""
    
    print("=" * 60)
    print("Testing show_table_ddl Tool")
    print("=" * 60)
    print()
    
    # First, get a table name to test with
    print("-" * 60)
    print("Step 1: Get a table name")
    print("-" * 60)
    try:
        tables_result = list_tables(env_name="shopee_sg_test", dbname="chatbot_api_db_sg")
        tables = json.loads(tables_result)
        if tables:
            test_table = tables[0]
            print(f"✓ Using table: {test_table}")
            print()
        else:
            print("✗ No tables found")
            return
    except Exception as e:
        print(f"✗ Failed to get tables: {e}")
        return
    
    # Test show_table_ddl
    print("-" * 60)
    print("Step 2: Show CREATE TABLE statement")
    print("-" * 60)
    print(f"Table: {test_table}")
    print()
    
    try:
        result = show_table_ddl(
            env_name="shopee_sg_test",
            dbname="chatbot_api_db_sg",
            table_name=test_table
        )
        ddl_info = json.loads(result)
        print("✓ Successfully retrieved table DDL")
        print()
        print("DDL Information:")
        print(json.dumps(ddl_info, indent=2, ensure_ascii=False))
        print()
        
        # If there's a Create Table statement, print it formatted
        if "Create Table" in ddl_info:
            print("-" * 60)
            print("Formatted CREATE TABLE statement:")
            print("-" * 60)
            print(ddl_info["Create Table"])
            print()
    except Exception as e:
        print(f"✗ Failed to get table DDL: {e}")
        print()
    
    # Summary
    print("=" * 60)
    print("Test completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
