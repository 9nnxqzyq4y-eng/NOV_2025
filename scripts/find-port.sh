#!/bin/bash
# Find available port and start dev server

PORT${1:-3000}

# Check if port is in use
if lsof -Pi :$PORT -sTCP:LISTEN -t /dev/null; then
  echo "⚠️  Port $PORT is in use"
  
  # Find next available port
  while lsof -Pi :$PORT -sTCP:LISTEN -t /dev/null; do
    PORT$((PORT + 1))
  done
  
  echo "✅ Using available port: $PORT"
fi

# Start dev server on available port
PORT$PORT npm run dev
