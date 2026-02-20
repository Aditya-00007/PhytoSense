"""
Database adapter that uses SQLAlchemy when available and falls back to local JSON storage
when SQLAlchemy is not installed or configured
"""
import os
import importlib.util
import sys
import json
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check if SQLAlchemy is available
sqlalchemy_available = importlib.util.find_spec("sqlalchemy") is not None
psycopg2_available = importlib.util.find_spec("psycopg2") is not None
database_url_available = bool(os.getenv("DATABASE_URL"))

# Determine if we can use SQLAlchemy
use_sqlalchemy = sqlalchemy_available and psycopg2_available and database_url_available

if use_sqlalchemy:
    try:
        logger.info("Using PostgreSQL database")
        print("Using PostgreSQL database")
        from database import (
            create_user, verify_user, update_user_profile, save_analysis,
            get_user_analyses, get_user_by_id, get_user_profile
        )
    except Exception as e:
        use_sqlalchemy = False
        logger.error(f"Failed to import database functions from SQLAlchemy module: {e}")
        logger.error(traceback.format_exc())
        print("Error setting up PostgreSQL, falling back to local database")

if not use_sqlalchemy:
    logger.info("Using local JSON database")
    print("Using local JSON database")
    from local_db import (
        create_user, verify_user, update_user_profile, save_analysis,
        get_user_analyses, get_user_by_id, get_user_profile
    )

# Function to get database type for UI display
def get_database_type():
    """Return a string indicating which database backend is in use"""
    return "PostgreSQL" if use_sqlalchemy else "Local JSON"