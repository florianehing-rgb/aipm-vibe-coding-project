#!/bin/bash
echo "Starting Vinyl Scout..."
cd "$(dirname "$0")"
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py
