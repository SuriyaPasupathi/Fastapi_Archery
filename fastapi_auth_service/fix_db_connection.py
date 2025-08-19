#!/usr/bin/env python3
"""
Fix Database Connection Script
This script will help fix the PostgreSQL connection issue.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def fix_connection():
    """Fix the database connection by creating the correct user"""
    
    print("🔧 Fixing PostgreSQL connection...")
    
    # Try to connect as postgres user (this should work since pgAdmin is connected)
    # We'll try different common passwords for the postgres user
    
    postgres_passwords = [
        '',  # No password
        'postgres',
        'admin',
        'password',
        '123456',
        'root',
        'postgresql',
        'postgres123',
        'admin123',
        '1234'  # Try the same password as the target user
    ]
    
    for password in postgres_passwords:
        try:
            print(f"Trying to connect as postgres with password: {'(empty)' if password == '' else password}")
            
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password=password
            )
            
            print(f"✅ Successfully connected as postgres user!")
            
            # Set autocommit mode
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Create the user 'user' with password '1234'
            print("Creating user 'user' with password '1234'...")
            try:
                cursor.execute("CREATE USER \"user\" WITH PASSWORD '1234';")
                print("✅ User 'user' created successfully!")
            except psycopg2.errors.DuplicateObject:
                print("⚠️  User 'user' already exists, updating password...")
                cursor.execute("ALTER USER \"user\" WITH PASSWORD '1234';")
                print("✅ User 'user' password updated!")
            
            # Grant privileges on the archery database
            print("Granting privileges on archery database...")
            try:
                cursor.execute("GRANT ALL PRIVILEGES ON DATABASE archery TO \"user\";")
                print("✅ Privileges granted!")
            except Exception as e:
                print(f"⚠️  Could not grant privileges: {e}")
            
            # Grant schema privileges
            try:
                cursor.execute("GRANT ALL ON SCHEMA public TO \"user\";")
                cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \"user\";")
                cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO \"user\";")
                print("✅ Schema privileges granted!")
            except Exception as e:
                print(f"⚠️  Could not grant schema privileges: {e}")
            
            cursor.close()
            conn.close()
            
            print("\n🎉 Database connection fixed!")
            print("Your .env file should work with:")
            print("DATABASE_URL=postgresql://user:1234@localhost/archery")
            
            return True
            
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                print("❌ Wrong password")
            else:
                print(f"❌ Connection error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n❌ Could not connect as postgres user.")
    print("\nAlternative solution:")
    print("Since pgAdmin is working, you can manually create the user:")
    print("1. Open pgAdmin")
    print("2. Right-click on 'Login/Group Roles'")
    print("3. Create new login role named 'user' with password '1234'")
    print("4. Grant all privileges on 'archery' database to 'user'")
    
    return False

if __name__ == "__main__":
    fix_connection()
