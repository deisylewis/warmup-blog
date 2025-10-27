#!/usr/bin/env python3
"""
Test script to verify the CSV Download and OpenAI Processing Application installation
"""

import sys
import os
import importlib

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Requires Python 3.7+")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\n📦 Testing dependencies...")
    
    dependencies = [
        'requests',
        'pandas',
        'openai',
        'dotenv',
        'schedule'
    ]
    
    all_good = True
    for dep in dependencies:
        try:
            if dep == 'dotenv':
                importlib.import_module('dotenv')
            else:
                importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - not installed")
            all_good = False
    
    return all_good

def test_modules():
    """Test if application modules can be imported"""
    print("\n🔧 Testing application modules...")
    
    modules = [
        'csv_downloader',
        'openai_processor',
        'main'
    ]
    
    all_good = True
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}.py")
        except ImportError as e:
            print(f"❌ {module}.py - {e}")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'main.py',
        'csv_downloader.py',
        'openai_processor.py',
        'scheduler.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - missing")
            all_good = False
    
    return all_good

def test_env_file():
    """Test environment file configuration"""
    print("\n⚙️ Testing environment configuration...")
    
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Check if it has required keys (even if empty)
        with open('.env', 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content:
                print("✅ OPENAI_API_KEY found in .env")
            else:
                print("⚠️ OPENAI_API_KEY not found in .env (you'll need to add this)")
        
        return True
    else:
        print("⚠️ .env file not found. Run setup.sh or copy .env.example to .env")
        return False

def test_directories():
    """Test if required directories exist or can be created"""
    print("\n📂 Testing directories...")
    
    dirs = ['downloads', 'processed']
    all_good = True
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            try:
                os.makedirs(dir_name)
                print(f"✅ {dir_name}/ directory created")
            except Exception as e:
                print(f"❌ Failed to create {dir_name}/ directory: {e}")
                all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🧪 CSV Download and OpenAI Processing Application - Installation Test\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Application Modules", test_modules),
        ("File Structure", test_file_structure),
        ("Environment Configuration", test_env_file),
        ("Directories", test_directories)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    
    if all_passed:
        print("🎉 All tests passed! Your installation is ready to use.")
        print("\nNext steps:")
        print("1. Add your API keys to the .env file")
        print("2. Run: python3 main.py --help")
        print("3. Try a test run: python3 main.py --download-only")
    else:
        print("⚠️ Some tests failed. Please address the issues above.")
        print("\nTroubleshooting:")
        print("- Run: ./setup.sh")
        print("- Install missing dependencies: pip3 install -r requirements.txt")
        print("- Check file permissions and Python installation")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())