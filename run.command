#!/bin/bash

# The Wisdom Council - Double-Click Startup (macOS)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

chmod +x run.py
python3 run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Press Enter to close this window..."
    read
fi
