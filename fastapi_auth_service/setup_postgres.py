#!/usr/bin/env python3
"""
PostgreSQL Setup Script for FastAPI Auth Service
This script helps set up the PostgreSQL database and user.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def setup_postgres():
    """Set up PostgreSQL database and user"""
    
    # Default PostgreSQL connection (usually works with default postgres user)
    default_connection = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': '1234'  # Try common default password
    }
    
    # Target database and user
    target_db = 'archery'
    target_user = 'user'
    target_password = '1234'
    
    try:
        print("Attempting to connect to PostgreSQL as postgres user...")
        
        # Try to connect with default postgres user
        conn = psycopg2.connect(**default_connection)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Successfully connected to PostgreSQL!")
        
        # Create user if it doesn't exist
        print(f"Creating user '{target_user}'...")
        try:
            cursor.execute(f"CREATE USER {target_user} WITH PASSWORD '{target_password}';")
            print(f"✅ User '{target_user}' created successfully!")
        except psycopg2.errors.DuplicateObject:
            print(f"⚠️  User '{target_user}' already exists, updating password...")
            cursor.execute(f"ALTER USER {target_user} WITH PASSWORD '{target_password}';")
            print(f"✅ User '{target_user}' password updated!")
        
        # Create database if it doesn't exist
        print(f"Creating database '{target_db}'...")
        try:
            cursor.execute(f"CREATE DATABASE {target_db} OWNER {target_user};")
            print(f"✅ Database '{target_db}' created successfully!")
        except psycopg2.errors.DuplicateDatabase:
            print(f"⚠️  Database '{target_db}' already exists!")
        
        # Grant privileges
        print("Granting privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {target_db} TO {target_user};")
        print("✅ Privileges granted!")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL setup completed successfully!")
        print(f"Database: {target_db}")
        print(f"User: {target_user}")
        print(f"Password: {target_password}")
        print("\nYour .env file should have:")
        print(f"DATABASE_URL=postgresql://{target_user}:{target_password}@localhost/{target_db}")
        
    except psycopg2.OperationalError as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
        print("\nPossible solutions:")
        print("1. Make sure PostgreSQL is running")
        print("2. Try connecting with different credentials")
        print("3. Check if PostgreSQL is installed correctly")
        
        # Try alternative connection methods
        print("\nTrying alternative connection methods...")
        
        # Try without password
        try:
            alt_connection = {
                'host': 'localhost',
                'port': 5432,
                'user': 'postgres'
            }
            conn = psycopg2.connect(**alt_connection)
            print("✅ Connected without password!")
            conn.close()
        except:
            print("❌ Could not connect without password either")
            
        print("\nPlease manually set up PostgreSQL:")
        print("1. Open pgAdmin or psql")
        print("2. Create a user named 'user' with password '1234'")
        print("3. Create a database named 'archery'")
        print("4. Grant all privileges on 'archery' to 'user'")

if __name__ == "__main__":
    setup_postgres()
