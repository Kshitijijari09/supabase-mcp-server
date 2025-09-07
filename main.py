#!/usr/bin/env python3
"""
Fixed Supabase MCP Server - Compatible with latest MCP versions
"""

import asyncio
import json
import logging
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent
from mcp.server.models import InitializationOptions, ServerCapabilities

from config import get_supabase_client, KNOWN_TABLES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("supabase-mcp")


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List all available database tables as MCP resources"""
    logger.info("Listing database resources...")

    resources = []
    for table in KNOWN_TABLES:
        resources.append(
            Resource(
                uri=f"supabase://tables/{table}",
                name=f"📊 {table.title()} Table",
                description=f"Access data from the {table} table in Supabase",
                mimeType="application/json"
            )
        )

    logger.info(f"Found {len(resources)} table resources")
    return resources


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read data from a specific database table resource"""
    logger.info(f"Reading resource: {uri}")

    try:
        if uri.startswith("supabase://tables/"):
            table_name = uri.split("/")[-1]

            if table_name not in KNOWN_TABLES:
                return json.dumps({
                    "error": f"Table '{table_name}' not found in known tables",
                    "available_tables": KNOWN_TABLES
                }, indent=2)

            supabase = get_supabase_client()
            result = supabase.table(table_name).select("*").limit(50).execute()

            response = {
                "table": table_name,
                "row_count": len(result.data),
                "sample_data": result.data[:10],
                "all_data": result.data
            }

            logger.info(
                f"Successfully read {len(result.data)} rows from {table_name}")
            return json.dumps(response, indent=2, default=str)

        return json.dumps({"error": f"Unknown resource URI: {uri}"}, indent=2)

    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return json.dumps({"error": str(e)}, indent=2)


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Define all available MCP tools for database operations"""
    return [
        Tool(
            name="query_table",
            description="Query any table with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": f"Table to query. Available: {', '.join(KNOWN_TABLES)}"
                    },
                    "columns": {
                        "type": "string",
                        "description": "Columns to select (default: '*')",
                        "default": "*"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum rows to return",
                        "default": 20
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="insert_data",
            description="Insert new record into a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": f"Target table. Available: {', '.join(KNOWN_TABLES)}"
                    },
                    "data": {
                        "type": "object",
                        "description": "Data to insert as key-value pairs"
                    }
                },
                "required": ["table_name", "data"]
            }
        ),
        Tool(
            name="count_rows",
            description="Count total rows in a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": f"Table to count. Available: {', '.join(KNOWN_TABLES)}"
                    }
                },
                "required": ["table_name"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute the requested tool with given arguments"""
    logger.info(f"Executing tool: {name} with args: {arguments}")

    try:
        supabase = get_supabase_client()

        if name == "query_table":
            table_name = arguments["table_name"]
            columns = arguments.get("columns", "*")
            limit = arguments.get("limit", 20)

            if table_name not in KNOWN_TABLES:
                return [TextContent(
                    type="text",
                    text=f"❌ Table '{table_name}' not available. Known tables: {', '.join(KNOWN_TABLES)}"
                )]

            result = supabase.table(table_name).select(
                columns).limit(limit).execute()

            response = {
                "table": table_name,
                "query_params": {"columns": columns, "limit": limit},
                "row_count": len(result.data),
                "data": result.data
            }

            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2, default=str)
            )]

        elif name == "insert_data":
            table_name = arguments["table_name"]
            data = arguments["data"]

            if table_name not in KNOWN_TABLES:
                return [TextContent(
                    type="text",
                    text=f"❌ Table '{table_name}' not available. Known tables: {', '.join(KNOWN_TABLES)}"
                )]

            result = supabase.table(table_name).insert(data).execute()

            return [TextContent(
                type="text",
                text=f"✅ Successfully inserted into {table_name}:\n{json.dumps(result.data, indent=2, default=str)}"
            )]

        elif name == "count_rows":
            table_name = arguments["table_name"]

            if table_name not in KNOWN_TABLES:
                return [TextContent(
                    type="text",
                    text=f"❌ Table '{table_name}' not available. Known tables: {', '.join(KNOWN_TABLES)}"
                )]

            result = supabase.table(table_name).select(
                "*", count="exact").execute()

            return [TextContent(
                type="text",
                text=f"📊 Table '{table_name}' contains {result.count} total rows"
            )]

        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(
            type="text",
            text=f"❌ Error executing {name}: {str(e)}"
        )]


async def main():
    """Main function to run the MCP server"""
    logger.info("Starting Supabase MCP Server...")

    try:
        # Test database connection
        supabase = get_supabase_client()
        logger.info("✅ Successfully connected to Supabase")

        # Start MCP server with a single, reliable initialization method
        async with stdio_server() as (read_stream, write_stream):
            logger.info("🚀 MCP Server running...")

            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="supabase-mcp",
                    server_version="1.0.0",
                    capabilities=ServerCapabilities(
                        tools={},
                        resources={}
                    )
                )
            )

    except Exception as e:
        logger.error(f"Failed to start server: {e}")

        # Provide helpful error information
        print("\n" + "="*50)
        print("🚨 MCP Server Failed to Start")
        print("="*50)
        print(f"Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check your .env file has correct Supabase credentials")
        print("2. Update KNOWN_TABLES in config.py with your actual table names")
        print("3. Check MCP library version: pip list | grep mcp")
        print("\n📋 Your current tables in config.py:")
        print(f"   {KNOWN_TABLES}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
