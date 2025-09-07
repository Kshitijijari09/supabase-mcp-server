# Supabase MCP Server

A Model Context Protocol (MCP) server for integrating Supabase databases with AI assistants like Claude. Built for use with Cursor IDE.

## 🚀 Features

- **Database Queries**: Query any table with filtering and sorting
- **CRUD Operations**: Create, read, update, and delete records
- **Resource Access**: Tables exposed as MCP resources
- **Type Safety**: Full TypeScript-style schemas for tools
- **Error Handling**: Comprehensive error handling and logging
- **Cursor Integration**: Optimized for Cursor IDE workflow

## 📋 Prerequisites

- Python 3.8+
- Supabase account and project
- Cursor IDE
- Basic knowledge of MCP (Model Context Protocol)

## 🛠️ Setup Instructions for Cursor IDE

### 1. **Install Dependencies**

Open terminal in Cursor (`Terminal` → `New Terminal`) and run:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. **Configure Environment Variables**

1. Copy your Supabase credentials from [Supabase Dashboard](https://supabase.com/dashboard)
2. Edit the `.env` file with your actual values:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-or-service-key-here
```

### 3. **Update Table Configuration**

Edit `config.py` and update the `KNOWN_TABLES` list with your actual table names:

```python
KNOWN_TABLES: List[str] = [
    "your_table_1",
    "your_table_2", 
    "your_table_3",
    # Add all your table names here
]
```

### 4. **Test the Connection**

Run this in Cursor's terminal to test your setup:

```bash
python -c "from config import get_supabase_client; print('✅ Connection successful!' if get_supabase_client() else '❌ Connection failed!')"
```

### 5. **Run the MCP Server**

```bash
python main.py
```

You should see:
```
INFO:__main__:✅ Successfully connected to Supabase
INFO:__main__:🚀 MCP Server running...
```

## 🔧 Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `query_table` | Query table with filters | `table_name`, `columns`, `filter_column`, `filter_value`, `limit`, `order_by` |
| `insert_data` | Insert new records | `table_name`, `data` |
| `update_data` | Update existing records | `table_name`, `filter_column`, `filter_value`, `update_data` |
| `delete_data` | Delete records | `table_name`, `filter_column`, `filter_value` |
| `count_rows` | Count table rows | `table_name` |
| `get_table_info` | Get table information | None |

## 📖 Usage Examples

### Query a table:
```json
{
  "tool": "query_table",
  "arguments": {
    "table_name": "users",
    "columns": "id, email, created_at",
    "filter_column": "status",
    "filter_value": "active",
    "limit": 10,
    "order_by": "created_at",
    "ascending": false
  }
}
```

### Insert data:
```json
{
  "tool": "insert_data", 
  "arguments": {
    "table_name": "users",
    "data": {
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

## 🔗 Integrating with Cursor IDE

### Using with Claude in Cursor:

1. **Start the MCP server**: `python main.py`
2. **Configure Cursor**: Add MCP server to your Cursor configuration
3. **Use with AI**: The AI can now query your database directly

### Cursor-Specific Tips:

- Use **Ctrl+Shift+P** → "Python: Select Interpreter" to ensure Cursor uses your virtual environment
- Install the **Python extension** for better IntelliSense
- Use **Cursor's AI chat** to help debug database queries
- Set up **debugging** with F5 for easy troubleshooting

## 🐛 Troubleshooting

### Common Issues:

**Connection Failed:**
- ✅ Check your `.env` file has correct Supabase URL and key
- ✅ Ensure your Supabase project is active
- ✅ Verify your key has the right permissions

**Table Not Found:**
- ✅ Update `KNOWN_TABLES` in `config.py`
- ✅ Check table names are exact (case-sensitive)
- ✅ Ensure tables exist in your Supabase project

**Import Errors:**
- ✅ Activate your virtual environment
- ✅ Run `pip install -r requirements.txt`
- ✅ Check Python version is 3.8+

### Debugging in Cursor:

1. Set breakpoints in your code
2. Press **F5** to start debugging
3. Use **Debug Console** to inspect variables
4. Check **Terminal** for error logs

## 📁 Project Structure

```
supabase-mcp-server/
├── main.py              # Main MCP server implementation
├── config.py            # Configuration and Supabase client
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (your secrets)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🚦 Next Steps

1. **Add more tables** to `KNOWN_TABLES`
2. **Implement table schema discovery** for dynamic table listing
3. **Add authentication** for production use
4. **Create custom tools** for your specific use cases
5. **Set up RLS policies** in Supabase for security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- Check the [MCP Documentation](https://modelcontextprotocol.io)
- Visit [Supabase Docs](https://supabase.com/docs)
- Open an issue for bugs or feature requests

---

**Happy coding with Cursor IDE! 🎯**