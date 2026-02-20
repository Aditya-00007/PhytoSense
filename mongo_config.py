import os
import streamlit as st
from pymongo import MongoClient
import urllib.parse

def get_mongo_client():
    """
    Get MongoDB client connection
    """
    # Try to get URI from secrets or environment
    mongo_uri = st.secrets.get("MONGO_URI") or os.environ.get("MONGO_URI")
    
    if not mongo_uri:
        return None
        
    try:
        client = MongoClient(mongo_uri)
        # Test connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_database():
    """
    Get database instance
    """
    client = get_mongo_client()
    if client:
        # Get database name from URI or default
        db_name = st.secrets.get("MONGO_DB_NAME") or os.environ.get("MONGO_DB_NAME") or "phytosense_db"
        return client[db_name]
    return None
