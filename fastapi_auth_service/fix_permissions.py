#!/usr/bin/env python3
"""
Fix Database Permissions Script
This script will grant proper permissions to the user for the archery database.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def fix_permissions():
    """Fix database permissions for the user"""
    
    print("🔧 Fixing database permissions...")
    
    try:
        # Connect as postgres user
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='1234'  # We know this works
        )
        
        print("✅ Connected as postgres user")
        
        # Set autocommit mode
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Grant all privileges on the archery database
        print("Granting database privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE archery TO \"user\";")
        
        # Close current connection and connect to archery database
        cursor.close()
        conn.close()
        
        # Connect directly to archery database
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='1234',
            database='archery'
        )
        
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Grant schema privileges
        print("Granting schema privileges...")
        cursor.execute("GRANT ALL ON SCHEMA public TO \"user\";")
        
        # Grant privileges on all existing tables
        print("Granting table privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \"user\";")
        
        # Grant privileges on all sequences
        print("Granting sequence privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO \"user\";")
        
        # Grant privileges on all functions
        print("Granting function privileges...")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO \"user\";")
        
        # Set default privileges for future tables
        print("Setting default privileges...")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO \"user\";")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO \"user\";")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO \"user\";")
        
        # Make user the owner of the public schema
        print("Setting schema ownership...")
        cursor.execute("ALTER SCHEMA public OWNER TO \"user\";")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Database permissions fixed successfully!")
        print("The user 'user' now has full access to the archery database.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing permissions: {e}")
        return False

if __name__ == "__main__":
    fix_permissions()
