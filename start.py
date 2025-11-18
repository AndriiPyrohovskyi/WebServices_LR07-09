#!/usr/bin/env python3
import os
import sys

port = os.getenv("PORT", "8080")
print(f"Starting server on port {port}")

# Use python -m uvicorn to ensure it's found
os.execvp(sys.executable, [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", port])
