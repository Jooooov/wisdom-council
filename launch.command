#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
#   HIS DARK MATERIALS — WISDOM COUNCIL v3
#   Double-click this file to launch in Terminal
# ═══════════════════════════════════════════════════════════════════════
#
#   macOS: Right-click → Open (first time), then double-click normally.
#   First run: Qwen3-4B model downloads ~2.3 GB automatically.
#
# ═══════════════════════════════════════════════════════════════════════

# Go to the project folder (same folder as this script)
cd "$(dirname "$0")"

# ── Find python3 ────────────────────────────────────────────────────────
PYTHON=$(which python3 2>/dev/null)

if [ -z "$PYTHON" ]; then
    echo ""
    echo "  ✗  python3 not found."
    echo "     Install from https://python.org or via Homebrew:"
    echo "     brew install python3"
    echo ""
    read -p "  Press ENTER to close..."
    exit 1
fi

# ── Check mlx-lm via pip (NOT import — avoids Abort Trap on first check) ──
if ! $PYTHON -m pip show mlx-lm > /dev/null 2>&1; then
    echo ""
    echo "  ⚠  mlx-lm is not installed."
    echo "     It is required for the AI model (Qwen3-4B)."
    echo ""
    read -p "  Install now? (y/n): " INSTALL_MLX
    if [[ "$INSTALL_MLX" == "y" || "$INSTALL_MLX" == "Y" ]]; then
        echo "  Installing mlx-lm and psutil..."
        $PYTHON -m pip install mlx-lm psutil --quiet
        echo "  ✓  Done."
    else
        echo "  Skipping. Some features will not work without mlx-lm."
    fi
fi

# ── Check psutil via pip ────────────────────────────────────────────────
if ! $PYTHON -m pip show psutil > /dev/null 2>&1; then
    $PYTHON -m pip install psutil --quiet
fi

# ── Fix OpenMP duplicate lib conflict (numpy + mlx on macOS) ────────────
export KMP_DUPLICATE_LIB_OK=TRUE

# ── Launch ──────────────────────────────────────────────────────────────
exec $PYTHON council.py
