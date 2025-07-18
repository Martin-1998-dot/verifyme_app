#!/bin/bash
echo "🚀 Installing required packages..."
sudo apt update
sudo apt install -y python3 python3-pip sqlite3 php-cli
pip3 install flask flask_sqlalchemy flask_bcrypt
echo "✅ Packages installed."
