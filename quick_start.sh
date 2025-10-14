#!/bin/bash

# Quick Start Script for Upgraded Student Stress Predictor
# This script helps you set up and run your beautiful new app!

echo "╔════════════════════════════════════════════════════╗"
echo "║   🧠 Student Stress Predictor - Quick Start       ║"
echo "║   ✨ Now with Beautiful UI & Groq AI!            ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check Streamlit
if ! command_exists streamlit; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Streamlit found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 Groq AI Setup (Optional but Recommended)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if API key is set
if [ -n "$GROQ_API_KEY" ]; then
    echo "✅ GROQ_API_KEY environment variable is set!"
    echo "   Your app will use AI-powered recommendations! ⚡"
else
    # Check config file
    if grep -q '"api_key": "[^"]' ai_config.json 2>/dev/null; then
        echo "✅ API key found in ai_config.json"
        echo "   Your app will use AI-powered recommendations! ⚡"
    else
        echo "⚠️  No Groq API key found"
        echo ""
        echo "🆓 Get a FREE Groq API key (takes 2 minutes):"
        echo "   1. Visit: https://console.groq.com"
        echo "   2. Sign up (free, no credit card)"
        echo "   3. Create an API key"
        echo "   4. Set it with: export GROQ_API_KEY='your_key_here'"
        echo ""
        echo "   Or add it to ai_config.json"
        echo ""
        echo "💡 Without Groq: App will use smart rule-based recommendations"
        echo "   (still works great!)"
        echo ""
        
        # Ask if user wants to set key now
        read -p "Do you have a Groq API key to set now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter your Groq API key: " api_key
            export GROQ_API_KEY="$api_key"
            echo "✅ API key set for this session!"
            echo ""
            echo "💡 To make it permanent, add this to your ~/.zshrc or ~/.bashrc:"
            echo "   export GROQ_API_KEY='$api_key'"
        fi
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Testing AI Integration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -n "$GROQ_API_KEY" ] || grep -q '"api_key": "[^"]' ai_config.json 2>/dev/null; then
    read -p "Would you like to test the AI integration? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        python3 test_groq.py
        echo ""
        read -p "Press Enter to continue..." -s
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Launching App"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✨ Your app will open in your browser shortly..."
echo ""
echo "🎯 What's New:"
echo "   • Beautiful gradient UI with animations"
echo "   • Lightning-fast Groq AI recommendations"
echo "   • Smooth hover effects and transitions"
echo "   • Professional design"
echo ""
echo "📖 Tips:"
echo "   • Try different stress profiles"
echo "   • Hover over cards for cool effects"
echo "   • Enable dark mode in Streamlit settings"
echo ""
echo "🛑 To stop: Press Ctrl+C in this terminal"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

sleep 2

# Run the app
streamlit run app.py
