#!/bin/bash
# Double-click (Mac) to preview the website at http://localhost:8123
cd "$(dirname "$0")"
open "http://localhost:8123" 2>/dev/null &
python3 serve.py 8123
