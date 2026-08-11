#!/bin/bash
# FFUF Scanner Installation Script

echo "🔧 Installing FFUF Scanner..."

# Update system
sudo apt update

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

# Install FFUF
echo "📦 Installing FFUF..."
if command -v ffuf &> /dev/null; then
    echo "✅ FFUF already installed"
else
    sudo apt install ffuf -y || {
        echo "⚠️ FFUF not in apt, installing via Go..."
        go install github.com/ffuf/ffuf@latest
    }
fi

# Check SecLists (ঐচ্ছিক)
if [ ! -d "/usr/share/seclists" ]; then
    echo "📥 Downloading SecLists..."
    sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
fi

# Make script executable
chmod +x ffuf_scanner.py

echo "✅ Installation complete!"
echo "🚀 Run: python3 ffuf_scanner.py example.com"
