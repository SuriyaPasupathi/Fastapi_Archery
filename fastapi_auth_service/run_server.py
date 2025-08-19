#!/usr/bin/env python3
"""
Server runner script that keeps the FastAPI application running
"""

import subprocess
import sys
import time
import os

def run_server():
    """Run the FastAPI server and restart if it stops"""
    print("🚀 Starting FastAPI Auth Service...")
    print("📍 Server will run on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print()
    print("⚠️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    while True:
        try:
            # Start the server
            process = subprocess.run([
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--reload", 
                "--host", "0.0.0.0", 
                "--port", "8000"
            ], cwd=os.path.dirname(os.path.abspath(__file__)))
            
            if process.returncode != 0:
                print(f"❌ Server stopped with exit code: {process.returncode}")
                print("🔄 Restarting in 5 seconds...")
                time.sleep(5)
            else:
                print("✅ Server stopped normally")
                break
                
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_server()
