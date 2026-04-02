#!/bin/bash

echo "🚀 Installing EchoDB - PostgreSQL Real-time Logger"
echo "=================================================="

if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run EchoDB:"
echo "  1. source venv/bin/activate"
echo "  2. python main.py"
echo ""
