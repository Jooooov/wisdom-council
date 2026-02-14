#!/bin/bash

# Wisdom Council - Launcher Script
# Handles environment setup and starts the application

# Set working directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ===== ENVIRONMENT SETUP =====

# CRITICAL: Fix OpenMP duplicate library error (macOS issue)
export KMP_DUPLICATE_LIB_OK=TRUE

# Optional: Set Python path
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

# ===== BANNER =====
clear
echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║                     🧙‍♂️  THE WISDOM COUNCIL v2                                 ║"
echo "║                   DeepSeek-R1-8B with Portuguese + Reasoning                   ║"
echo "║                                                                                ║"
echo "║  Checking system requirements...                                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# ===== RAM CHECK =====
echo "📊 Checking available RAM..."

# Get available RAM in GB (macOS)
AVAILABLE_RAM=$(vm_stat | grep "Pages free" | awk '{print int($3) * 4096 / 1024 / 1024 / 1024}')
REQUIRED_RAM=7.5

echo "   Available: ${AVAILABLE_RAM}GB"
echo "   Required:  ${REQUIRED_RAM}GB minimum"
echo ""

# Check if sufficient RAM
if (( $(echo "$AVAILABLE_RAM < $REQUIRED_RAM" | bc -l) )); then
    echo "❌ INSUFFICIENT RAM!"
    echo ""
    echo "   Available: ${AVAILABLE_RAM}GB"
    echo "   Required:  ${REQUIRED_RAM}GB minimum"
    echo ""
    echo "💡 Solutions:"
    echo "   1. Close browser tabs and other applications"
    echo "   2. Close Slack, Discord, email clients"
    echo "   3. Close IDEs and text editors"
    echo "   4. Restart your MacBook"
    echo ""
    exit 1
fi

echo "✅ RAM check passed!"
echo ""

# ===== PYTHON CHECK =====
echo "🐍 Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo ""
    echo "💡 Please install Python 3:"
    echo "   brew install python3"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: ${PYTHON_VERSION}"
echo "✅ Python available"
echo ""

# ===== START APPLICATION =====
echo "🚀 Starting The Wisdom Council..."
echo ""
echo "═════════════════════════════════════════════════════════════════════════════════"
echo ""

# Run Python application
python3 run.py

# Capture exit code
EXIT_CODE=$?

echo ""
echo "═════════════════════════════════════════════════════════════════════════════════"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ The Wisdom Council has closed gracefully."
else
    echo "❌ The Wisdom Council closed with error code: $EXIT_CODE"
    echo ""
    echo "💡 If you see OpenMP errors, the environment is already set correctly."
    echo "   If you see RAM errors, please close other applications and try again."
fi

echo ""
exit $EXIT_CODE
