#!/bin/bash

# Deployment script for Ultrahuman MCP Server

echo "🚀 Preparing Ultrahuman MCP Server for deployment..."

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this script from the project root."
    exit 1
fi

# Initialize git repository if it doesn't exist
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Ultrahuman MCP Server"
fi

# Check for required environment variables
if [ -z "$ULTRAHUMAN_AUTH_KEY" ]; then
    echo "⚠️  Warning: ULTRAHUMAN_AUTH_KEY not set."
    echo "   Please set this environment variable before deploying."
fi

# Test Python dependencies
echo "🔍 Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    python3 -c "import fastmcp, httpx" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies check passed"
    else
        echo "⚠️  Installing dependencies..."
        pip3 install -r requirements.txt
    fi
else
    echo "❌ Error: Python 3 not found"
    exit 1
fi

# Test the server
echo "🧪 Testing server startup..."
timeout 10s python3 main.py &
SERVER_PID=$!
sleep 5

if kill -0 $SERVER_PID 2>/dev/null; then
    echo "✅ Server starts successfully"
    kill $SERVER_PID
else
    echo "❌ Server failed to start"
    exit 1
fi

echo ""
echo "✅ Deployment preparation complete!"
echo ""
echo "Next steps for Railway deployment:"
echo "1. Push this repository to GitHub"
echo "2. Connect GitHub repository to Railway"
echo "3. Set environment variable: ULTRAHUMAN_AUTH_KEY"
echo "4. Deploy the project with your chosen name"
echo ""
echo "Railway will automatically:"
echo "- Detect the Dockerfile"
echo "- Build and deploy the application"
echo "- Expose it on the assigned URL"
