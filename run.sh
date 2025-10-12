#!/bin/bash

# Student Stress Predictor - Run Script
# This script sets up and runs the complete application

echo "=========================================="
echo "Student Stress Predictor - Setup & Run"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "=========================================="
echo "Step 1: Data Ingestion"
echo "=========================================="
python3 scripts/ingest_multi_dataset.py

if [ $? -ne 0 ]; then
    echo "❌ Data ingestion failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "=========================================="
echo "Step 2: Model Training"
echo "=========================================="
python3 scripts/train_multi_dataset.py

if [ $? -ne 0 ]; then
    echo "❌ Model training failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "=========================================="
echo "Step 3: Starting Web Application"
echo "=========================================="
echo "The app will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

streamlit run app.py
