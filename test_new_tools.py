#!/usr/bin/env python3
"""
Test script for new Data Explorer tools: list_dbnames and list_tables.
"""
import json
import os

# Set up environment variables for testing
os.environ["DATA_EXPLORER_MODULE_NAME"] = "chatbot_admin"
os.environ["DATA_EXPLORER_SECRET"] = "9b5f618608db30b792a97bc03563baa0"

from tools.data_explorer import list_dbnames, list_tables


def main():
    """Test new Data Explorer tools."""
    
    print("=" * 60)
    print("Testing New Data Explorer Tools")
    print("=" * 60)
    print()
    
    # Test 1: list_dbnames
    print("-" * 60)
    print("Test 1: list_dbnames")
    print("-" * 60)
    try:
        result = list_dbnames(env_name="shopee_sg_test")
        databases = json.loads(result)
        print(f"✓ Successfully retrieved {len(databases)} database(s)")
        print("\nFirst 10 databases:")
        print(json.dumps(databases[:10], indent=2))
        print()
        
        # Save first database for next test
        test_dbname = databases[0] if databases else None
    except Exception as e:
        print(f"✗ Failed to list databases: {e}")
        print()
        test_dbname = None
    
    # Test 2: list_tables
    if test_dbname:
        print("-" * 60)
        print("Test 2: list_tables")
        print("-" * 60)
        print(f"Testing with database: {test_dbname}")
        print()
        
        try:
            result = list_tables(env_name="shopee_sg_test", dbname=test_dbname)
            tables = json.loads(result)
            print(f"✓ Successfully retrieved {len(tables)} table(s)")
            print("\nFirst 10 tables:")
            print(json.dumps(tables[:10], indent=2))
            print()
        except Exception as e:
            print(f"✗ Failed to list tables: {e}")
            print()
    else:
        print("-" * 60)
        print("Test 2: list_tables")
        print("-" * 60)
        print("⚠ Skipped: No database available for testing")
        print()
    
    # Summary
    print("=" * 60)
    print("Test completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
