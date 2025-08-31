#!/usr/bin/env python3
"""
Build script for web deployment using pygbag
"""
import subprocess
import sys
import os

def install_pygbag():
    """Install pygbag for web builds"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pygbag"], check=True)
        print("✓ pygbag installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install pygbag")
        return False
    return True

def build_web():
    """Build the game for web deployment"""
    try:
        cmd = [
            sys.executable, "-m", "pygbag",
            "main.py",
            "--width", "1280",
            "--height", "720", 
            "--name", "Ashley's Asteroids",
            "--archive"
        ]
        subprocess.run(cmd, check=True)
        print("✓ Web build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Web build failed: {e}")
        return False

if __name__ == "__main__":
    print("Building Ashley's Asteroids for web deployment...")
    
    if not install_pygbag():
        sys.exit(1)
        
    if not build_web():
        sys.exit(1)
        
    print("🚀 Build complete! Check the 'dist' folder for web files.")