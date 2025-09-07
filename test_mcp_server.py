#!/usr/bin/env python3
"""
Test script for Supabase MCP Server
Tests all available tools and functionality
"""

import asyncio
import json
import sys
from typing import Dict, Any

# Import the server functions directly
from main import (
    handle_list_resources,
    handle_list_tools,
    handle_call_tool
)
from config import get_supabase_client, KNOWN_TABLES


async def test_list_resources():
    """Test the list_resources functionality"""
    print("🔍 Testing list_resources...")
    try:
        resources = await handle_list_resources()
        print(f"✅ Found {len(resources)} resources:")
        for resource in resources:
            print(f"   - {resource.name}: {resource.description}")
        return True
    except Exception as e:
        print(f"❌ Error testing list_resources: {e}")
        return False


async def test_list_tools():
    """Test the list_tools functionality"""
    print("\n🔧 Testing list_tools...")
    try:
        tools = await handle_list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        return True
    except Exception as e:
        print(f"❌ Error testing list_tools: {e}")
        return False


async def test_tool_execution():
    """Test tool execution with sample data"""
    print("\n⚡ Testing tool execution...")

    # Test get_table_info
    print("   Testing get_table_info...")
    try:
        result = await handle_call_tool("get_table_info", {})
        print(f"   ✅ get_table_info: {result[0].text}")
    except Exception as e:
        print(f"   ❌ get_table_info error: {e}")

    # Test count_rows for each table
    print("   Testing count_rows...")
    for table in KNOWN_TABLES[:2]:  # Test first 2 tables
        try:
            result = await handle_call_tool("count_rows", {"table_name": table})
            print(f"   ✅ count_rows({table}): {result[0].text}")
        except Exception as e:
            print(f"   ❌ count_rows({table}) error: {e}")

    # Test query_table
    print("   Testing query_table...")
    try:
        result = await handle_call_tool("query_table", {
            "table_name": KNOWN_TABLES[0],
            "limit": 3
        })
        print(f"   ✅ query_table: {result[0].text}")
    except Exception as e:
        print(f"   ❌ query_table error: {e}")


def test_database_connection():
    """Test direct database connection"""
    print("\n🗄️  Testing database connection...")
    try:
        client = get_supabase_client()

        # Test a simple query on each table
        for table in KNOWN_TABLES[:2]:  # Test first 2 tables
            try:
                result = client.table(table).select("*").limit(1).execute()
                print(
                    f"   ✅ Table '{table}': {len(result.data)} rows accessible")
            except Exception as e:
                print(f"   ⚠️  Table '{table}': {str(e)[:100]}...")

        return True
    except Exception as e:
        print(f"   ❌ Database connection error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🧪 Supabase MCP Server Test Suite")
    print("=" * 50)

    # Test database connection
    db_ok = test_database_connection()

    # Test MCP server functions
    resources_ok = await test_list_resources()
    tools_ok = await test_list_tools()

    # Test tool execution
    await test_tool_execution()

    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Database Connection: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"   List Resources: {'✅ PASS' if resources_ok else '❌ FAIL'}")
    print(f"   List Tools: {'✅ PASS' if tools_ok else '❌ FAIL'}")

    if db_ok and resources_ok and tools_ok:
        print("\n🎉 All tests passed! Your MCP server is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
