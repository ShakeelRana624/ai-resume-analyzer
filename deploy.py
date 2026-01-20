#!/usr/bin/env python3
"""
Streamlit Cloud Deployment Script for AI Resume Analyzer
Deploy to Streamlit Cloud for free hosting
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def run_streamlit():
    """Run Streamlit app"""
    print("🚀 Starting Streamlit app...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def main():
    """Main deployment function"""
    print("🌟 AI Resume Analyzer - Streamlit Cloud Deployment")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Exiting...")
        return
    
    print("\n📝 Installation complete!")
    print("\n🌐 App will be available at: http://localhost:8501")
    print("\n💡 To deploy to Streamlit Cloud:")
    print("   1. Push code to GitHub")
    print("   2. Connect Streamlit Cloud account")
    print("   3. Deploy from GitHub repository")
    print("\n🔗 Local URL: http://localhost:8501")
    print("\n📱 Share this link for others to access your app!")
    
    # Run the app
    run_streamlit()

if __name__ == "__main__":
    main()
