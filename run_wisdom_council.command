#!/bin/bash

# Wisdom Council - Double-click launcher for macOS
# This file can be double-clicked in Finder to start the application

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the main launcher script
"${SCRIPT_DIR}/run_wisdom_council.sh"
