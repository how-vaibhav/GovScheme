#!/bin/bash
# Start both Django and RASA servers automatically
# This script is for Linux/Mac systems

echo ""
echo "===================================================="
echo "    GOVERNMENT SCHEMES PORTAL - AUTO STARTUP"
echo "===================================================="
echo ""

cd "~/OneDrive/Desktop/GovScheme" || cd "/home/user/GovScheme"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
fi

echo "Starting servers..."
python3 run_all_servers.py
