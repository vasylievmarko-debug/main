#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "Installing Python dependencies..."
pip install -q -r "$CLAUDE_PROJECT_DIR/requirements.txt"

echo "Session start complete."
