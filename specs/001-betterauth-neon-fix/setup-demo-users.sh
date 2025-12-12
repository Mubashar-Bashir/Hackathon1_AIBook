#!/bin/bash

# Script to run the BetterAuth demo user creation process

set -e  # Exit on any error

echo "==========================================="
echo "BetterAuth Demo User Creation Tool"
echo "==========================================="

# Check if required environment variable is set
if [ -z "$NEON_DATABASE_URL" ]; then
    echo "ERROR: NEON_DATABASE_URL environment variable not set"
    echo "Please set your Neon database URL:"
    echo "export NEON_DATABASE_URL=\"your_neon_database_connection_string\""
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "ERROR: pip is not installed or not in PATH"
    exit 1
fi

echo "Installing required dependencies..."
pip install -r requirements.txt

echo ""
echo "Creating demo users..."
python3 demo-users-script.py

echo ""
echo "Verifying created users..."
python3 verify-users.py

echo ""
echo "==========================================="
echo "Demo user creation process completed!"
echo "You can now test sign-in functionality with the created users."
echo "==========================================="