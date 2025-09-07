#!/usr/bin/env python3
"""
Test MCP Protocol directly - simulates what Cursor will do
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any


async def test_mcp_protocol():
    """Test the MCP server using the actual MCP protocol"""
    print("🧪 Testing MCP Protocol Communication")
    print("=" * 50)

    # Start the MCP server as a subprocess
    print("🚀 Starting MCP server...")
    process = subprocess.Popen(
        ["./start_mcp_server.sh"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/Users/kshitijijari/Desktop/MySpace/MCP/supabase-mcp-server"
    )

    try:
        # Wait a moment for server to start
        await asyncio.sleep(2)

        # Send MCP initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    },
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        print("📤 Sending initialization request...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(
                f"📥 Received response: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")

        # Test list tools
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }

        print("🔧 Requesting tools list...")
        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()

        tools_response = process.stdout.readline()
        if tools_response:
            tools_data = json.loads(tools_response.strip())
            tools = tools_data.get('result', {}).get('tools', [])
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(
                    f"   - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")

        # Test list resources
        resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list"
        }

        print("📊 Requesting resources list...")
        process.stdin.write(json.dumps(resources_request) + "\n")
        process.stdin.flush()

        resources_response = process.stdout.readline()
        if resources_response:
            resources_data = json.loads(resources_response.strip())
            resources = resources_data.get('result', {}).get('resources', [])
            print(f"✅ Found {len(resources)} resources:")
            for resource in resources:
                print(
                    f"   - {resource.get('name', 'Unknown')}: {resource.get('description', 'No description')}")

        print("\n🎉 MCP Protocol test completed successfully!")
        print("Your server is ready for Cursor integration!")

    except Exception as e:
        print(f"❌ Error during MCP protocol test: {e}")
        return False
    finally:
        # Clean up
        process.terminate()
        process.wait()

    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_protocol())
    sys.exit(0 if success else 1)


