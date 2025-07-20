#!/bin/bash

# CSV Download and OpenAI Processing Application Setup Script

echo "🚀 Setting up CSV Download and OpenAI Processing Application..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.7+ and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed. Please install pip and try again."
    exit 1
fi

# Use pip3 if available, otherwise pip
PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo "✅ pip found: $($PIP_CMD --version)"

# Install dependencies
echo "📦 Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your API keys:"
    echo "   - OPENAI_API_KEY (required)"
    echo "   - RB2B_API_KEY and RB2B_API_URL (optional)"
    echo "   - HEYREACH_API_KEY and HEYREACH_API_URL (optional)"
    echo ""
    echo "   Edit the file: nano .env"
else
    echo "✅ .env file already exists"
fi

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p downloads processed
echo "✅ Directories created"

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x main.py scheduler.py
echo "✅ Scripts made executable"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit your .env file with API keys: nano .env"
echo "2. Run a test: python3 main.py --download-only"
echo "3. Run full pipeline: python3 main.py"
echo "4. Schedule automated runs: python3 scheduler.py --schedule-type daily"
echo ""
echo "For help: python3 main.py --help"
echo "For scheduler help: python3 scheduler.py --help"
echo ""
echo "Happy analyzing! 📊"