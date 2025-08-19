#!/usr/bin/env python3
"""
Try common PostgreSQL passwords for the postgres user
"""

import psycopg2
import sys

def try_common_passwords():
    """Try common passwords for PostgreSQL postgres user"""
    
    common_passwords = [
        '',  # No password
        'postgres',
        'admin',
        'password',
        '123456',
        'root',
        'postgresql',
        'postgres123',
        'admin123'
    ]
    
    print("Trying common passwords for PostgreSQL postgres user...")
    
    for password in common_passwords:
        try:
            print(f"Trying password: {'(empty)' if password == '' else password}")
            
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password=password
            )
            
            print(f"✅ SUCCESS! Password is: {'(empty)' if password == '' else password}")
            
            # Test if we can create the database and user
            cursor = conn.cursor()
            
            # Create user
            try:
                cursor.execute("CREATE USER \"user\" WITH PASSWORD '1234';")
                print("✅ Created user 'user'")
            except psycopg2.errors.DuplicateObject:
                print("⚠️  User 'user' already exists, updating password...")
                cursor.execute("ALTER USER \"user\" WITH PASSWORD '1234';")
                print("✅ Updated user 'user' password")
            
            # Create database
            try:
                cursor.execute("CREATE DATABASE archery OWNER \"user\";")
                print("✅ Created database 'archery'")
            except psycopg2.errors.DuplicateDatabase:
                print("⚠️  Database 'archery' already exists")
            
            # Grant privileges
            cursor.execute("GRANT ALL PRIVILEGES ON DATABASE archery TO \"user\";")
            print("✅ Granted privileges")
            
            cursor.close()
            conn.close()
            
            print("\n🎉 PostgreSQL setup completed successfully!")
            print("You can now start your FastAPI application.")
            return True
            
        except psycopg2.OperationalError as e:
            if "password authentication failed" in str(e):
                print("❌ Wrong password")
            else:
                print(f"❌ Connection error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n❌ Could not connect with any common password.")
    print("\nPlease try one of these solutions:")
    print("1. Open pgAdmin and connect to PostgreSQL")
    print("2. Create user 'user' with password '1234'")
    print("3. Create database 'archery'")
    print("4. Grant all privileges on 'archery' to 'user'")
    print("\nOr try connecting with your actual postgres password:")
    print("psql -U postgres -h localhost")
    
    return False

if __name__ == "__main__":
    try_common_passwords()
