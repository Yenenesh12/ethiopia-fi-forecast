"""
Setup script for Ethiopia Digital Finance Analysis
"""

import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directory structure...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "figures",
        "tables",
        "reports/figures",
        "models",
        "dashboard"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    print("✅ Directory structure ready!")

def main():
    """Main setup function"""
    print("🚀 ETHIOPIA DIGITAL FINANCE ANALYSIS SETUP")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if install_requirements():
        print("\n✅ SETUP COMPLETE!")
        print("=" * 30)
        print("🎯 Next Steps:")
        print("   1. Run analysis: python run_analysis.py")
        print("   2. Launch dashboard: streamlit run dashboard/app.py")
        print("   3. View results in figures/ and tables/")
    else:
        print("\n❌ Setup failed. Please install requirements manually.")

if __name__ == "__main__":
    main()