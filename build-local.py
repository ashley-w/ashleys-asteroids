#!/usr/bin/env python3
"""
Simple local build script for manual deployment
"""
import subprocess
import sys
import os

def build_game():
    """Build game locally with basic settings"""
    print("Building Ashley's Asteroids locally...")
    
    try:
        # Install dependencies if needed
        subprocess.run([sys.executable, "-m", "pip", "install", "pygame-ce", "pygbag"], check=False)
        
        # Simple pygbag build (no extra flags to avoid issues)
        result = subprocess.run([
            sys.executable, "-m", "pygbag", 
            "main.py"
        ], timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✅ Build successful!")
            print("📁 Check the 'main' folder for web files")
            print("🌐 Upload the contents to Netlify manually")
        else:
            print("❌ Build failed")
            
    except subprocess.TimeoutExpired:
        print("⏰ Build timed out after 5 minutes")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    build_game()