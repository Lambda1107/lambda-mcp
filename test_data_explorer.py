#!/usr/bin/env python3
"""
Test script for DataExplorer client.
"""
import json
from lib.data_explorer_client import DataExplorer


def main():
    """Test DataExplorer functionality."""
    
    # Configuration
    module_name = "chatbot_admin"
    secret = "9b5f618608db30b792a97bc03563baa0"
    base_url = "https://data-service.test.sz.shopee.io/api/v1/service/"
    
    print("=" * 60)
    print("DataExplorer Test Script")
    print("=" * 60)
    print(f"Module Name: {module_name}")
    print(f"Base URL: {base_url}")
    print("=" * 60)
    print()
    
    # Create DataExplorer client
    try:
        explorer = DataExplorer(
            secret=secret,
            module_name=module_name,
            base_url=base_url
        )
        print("✓ DataExplorer client created successfully")
        print()
    except Exception as e:
        print(f"✗ Failed to create DataExplorer client: {e}")
        return
    
    # Test 1: Explore databases
    print("-" * 60)
    print("Test 1: Explore Databases (explore_db)")
    print("-" * 60)
    try:
        databases = explorer.explore_db()
        print(f"✓ Successfully retrieved {len(databases)} database(s)")
        print("\nAvailable databases:")
        print(json.dumps(databases, indent=2))
        print()
    except Exception as e:
        print(f"✗ Failed to explore databases: {e}")
        print()
        databases = []
    
    # Test 2: Query database (if databases are available)
    if databases:
        print("-" * 60)
        print("Test 2: Query Database (query_db)")
        print("-" * 60)
        
        # Use the first database for testing
        test_dbname = databases[0] if isinstance(databases[0], str) else databases[0].get('name', databases[0].get('dbname', 'unknown'))
        test_sql = "SHOW TABLES"
        
        print(f"Database: {test_dbname}")
        print(f"SQL: {test_sql}")
        print()
        
        try:
            results = explorer.query_db(test_dbname, test_sql)
            print(f"✓ Query executed successfully")
            print(f"✓ Retrieved {len(results)} result(s)")
            print("\nQuery results:")
            print(json.dumps(results[:5], indent=2))  # Show first 5 results
            if len(results) > 5:
                print(f"\n... and {len(results) - 5} more results")
            print()
        except Exception as e:
            print(f"✗ Failed to query database: {e}")
            print()
    else:
        print("-" * 60)
        print("Test 2: Query Database (query_db)")
        print("-" * 60)
        print("⚠ Skipped: No databases available for testing")
        print()
    
    # Summary
    print("=" * 60)
    print("Test completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
