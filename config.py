"""
Configuration file for Supabase MCP Server
"""

import os
from typing import List
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate environment variables
if not SUPABASE_URL:
    raise ValueError("❌ SUPABASE_URL not found in environment variables. Please check your .env file.")

if not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_KEY not found in environment variables. Please check your .env file.")

# Known tables in your database
# TODO: Replace these with your actual table names
KNOWN_TABLES: List[str] = [
    "users",           # Example: User accounts
    "vendors",           # Example: Blog posts or content
    "businesses",        # Example: User comments
    "connections",        # Example: User profiles
    "documents",
    "messages",
    "reviews",
    "chat_sessions"      # Example: Content categories
    # Add your actual table names here
]

def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance
    
    Returns:
        Client: Configured Supabase client
    
    Raises:
        Exception: If connection fails
    """
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test the connection with a simple query
        # This will raise an exception if credentials are wrong
        client.auth.get_session()
        
        return client
    
    except Exception as e:
        raise Exception(f"Failed to connect to Supabase: {str(e)}")

def validate_table_name(table_name: str) -> bool:
    """
    Validate if a table name is in our known tables list
    
    Args:
        table_name (str): Name of the table to validate
    
    Returns:
        bool: True if table is valid, False otherwise
    """
    return table_name in KNOWN_TABLES

def get_table_list() -> List[str]:
    """
    Get the list of available tables
    
    Returns:
        List[str]: List of table names
    """
    return KNOWN_TABLES.copy()

# Optional: Database schema information
# You can add this if you want to provide schema information
TABLE_SCHEMAS = {
    "users": {
        "description": "User account information",
        "primary_key": "id",
        "common_columns": ["id", "email", "created_at", "updated_at"]
    },
    "posts": {
        "description": "Blog posts or content items",
        "primary_key": "id", 
        "common_columns": ["id", "title", "content", "author_id", "created_at"]
    },
    # Add schema info for your tables
}

def get_table_schema(table_name: str) -> dict:
    """
    Get schema information for a table
    
    Args:
        table_name (str): Name of the table
    
    Returns:
        dict: Schema information or empty dict if not found
    """
    return TABLE_SCHEMAS.get(table_name, {})