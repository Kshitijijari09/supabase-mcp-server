# Cursor IDE Integration Guide

## 🚀 How to Integrate Your Supabase MCP Server with Cursor

### Step 1: Add MCP Configuration to Cursor

1. **Open Cursor Settings**:

   - Press `Cmd+,` (macOS) or `Ctrl+,` (Windows/Linux)
   - Or go to `Cursor` → `Preferences` → `Settings`

2. **Find MCP Settings**:

   - Search for "MCP" in the settings search bar
   - Look for "MCP Servers" or "Model Context Protocol" settings

3. **Add Your Server Configuration**:
   Copy the contents of `cursor-mcp-config.json` into your Cursor MCP settings:

   ```json
   {
     "mcpServers": {
       "supabase-mcp": {
         "command": "/Users/kshitijijari/Desktop/MySpace/MCP/supabase-mcp-server/start_mcp_server.sh",
         "args": []
       }
     }
   }
   ```

### Step 2: Restart Cursor

After adding the configuration, restart Cursor completely to load the MCP server.

### Step 3: Test the Integration

1. **Open Cursor Chat** (usually `Cmd+L` or `Ctrl+L`)
2. **Ask the AI to query your database**:

   Example prompts:

   - "How many users are in my database?"
   - "Show me the first 5 users from my Supabase database"
   - "What tables are available in my database?"
   - "Count the vendors in my database"

### Step 4: Verify MCP Server is Running

The AI should be able to:

- ✅ List your database tables
- ✅ Query data from your tables
- ✅ Count records
- ✅ Insert new data (if you have write permissions)

## 🔧 Troubleshooting

### If the MCP server doesn't start:

1. **Check the startup script**:

   ```bash
   cd /Users/kshitijijari/Desktop/MySpace/MCP/supabase-mcp-server
   ./start_mcp_server.sh
   ```

2. **Verify virtual environment**:

   ```bash
   source mcp-venv/bin/activate
   python main.py
   ```

3. **Check Cursor logs**:
   - Look in Cursor's developer console for MCP-related errors
   - Check if the server process is running: `ps aux | grep main.py`

### If the AI can't access your database:

1. **Verify your `.env` file** has correct Supabase credentials
2. **Check table names** in `config.py` match your actual tables
3. **Test database connection**:
   ```bash
   python test_mcp_server.py
   ```

## 🎯 Example Usage

Once integrated, you can ask Cursor's AI things like:

- "Show me all active users"
- "How many vendors do I have?"
- "What's the structure of my users table?"
- "Add a new user with email test@example.com"
- "Find users created in the last week"

The AI will use your MCP server to directly query your Supabase database!

## 📋 Available Tools

Your MCP server provides these tools to the AI:

1. **query_table** - Query any table with filtering
2. **count_rows** - Count records in a table
3. **insert_data** - Add new records
4. **update_data** - Modify existing records
5. **delete_data** - Remove records
6. **get_table_info** - Get table structure

## 🔒 Security Notes

- Your Supabase credentials are stored in `.env` file
- The MCP server only exposes the tables listed in `KNOWN_TABLES`
- Make sure your Supabase key has appropriate permissions
- Consider using Row Level Security (RLS) in Supabase for additional protection


