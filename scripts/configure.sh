#!/bin/bash

# Enhanced configuration script with better user guidance

echo "🚀 Multi-Agent DSL Framework Configuration Wizard"
echo "-----------------------------------------------"

# Check if .env exists
if [ -f .env ]; then
  echo "⚠️  Found existing .env file"
  read -p "Do you want to overwrite it? [y/N] " overwrite
  if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
    echo "ℹ️  Configuration cancelled. Using existing .env file"
    exit 0
  fi
fi

# Copy template
echo "📋 Creating .env file from template..."
cp -v .env.example .env

# Get API key
echo ""
echo "🔑 DeepSeek API Key Setup"
echo "1. Go to https://platform.deepseek.com"
echo "2. Login/Create account"
echo "3. Get your API key"
echo ""
read -p "Paste your API key here: " api_key

# Validate key format (basic check)
if [[ ! "$api_key" =~ ^sk-[a-zA-Z0-9]{32,50}$ ]]; then
  echo "❌ Invalid API key format. Should look like: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  exit 1
fi

# Update config
echo "⚙️  Updating configuration..."
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sed -i '' "s/DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=$api_key/" .env
else
  # Windows (Git Bash)
  sed -i "s/DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=$api_key/" .env
fi

# Success message
echo ""
echo "✅ Configuration complete!"
echo ""
echo "Next steps:"
echo "1. Start backend:"
echo "   uvicorn backend.main:app --reload"
echo "2. In a new terminal, start frontend:"
echo "   cd frontend && npm start"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "💡 Tip: If you need to edit the configuration later:"
echo "- Linux/macOS: Use './scripts/configure.sh' again"
echo "- Windows: Edit the .env file with Notepad or VS Code"
