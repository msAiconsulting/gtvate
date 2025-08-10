#!/bin/bash

echo "🎵 Starting Acoustic Sensor POC Dashboard..."
echo "=============================================="

# Check if UV virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ UV virtual environment not found. Creating one..."
    uv venv
fi

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python -c "import gradio, pandas, plotly" &> /dev/null; then
    echo "📥 Installing required packages..."
    uv pip install -r requirements.txt
fi

# Launch the dashboard
echo "🚀 Launching dashboard..."
echo "🌐 Dashboard will be available at: http://localhost:7860"
echo "🔄 Press Ctrl+C to stop the dashboard"
echo ""

python acoustic_dashboard.py 