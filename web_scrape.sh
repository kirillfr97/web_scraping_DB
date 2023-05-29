#!/bin/bash

# Checking existence of environment variable PYTHON_PATH
if [ -z "$PYTHON_PATH" ]; then
    echo "Environment variable PYTHON_PATH is not set"
    exit 1
fi

# Checking python executable in PYTHON_PATH
if [ ! -x "$PYTHON_PATH/python" ]; then
    echo "Python executable not found in path: $PYTHON_PATH"
    exit 1
fi

# Getting the directory of the script
batch_folder="$(cd "$(dirname "$0")" && pwd)"

# Start main.py
"$PYTHON_PATH/python" "$batch_folder/main.py"

echo "Done"
