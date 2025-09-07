#!/bin/bash
# Startup script for Supabase MCP Server with virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/mcp-venv/bin/activate"

# Run the MCP server
python "$SCRIPT_DIR/main.py"


