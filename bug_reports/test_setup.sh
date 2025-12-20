#!/bin/bash
# Test script to demonstrate the issue tracking system

echo "Testing Issue Tracking System"
echo "=============================="

echo "1. Checking directory structure..."
ls -la ../bug_reports/ | grep -E "(open|closed|resolved|metadata|templates)$"

echo ""
echo "2. Checking template files..."
ls -la ../bug_reports/templates/

echo ""
echo "3. Checking metadata report..."
ls -la ../bug_reports/metadata/

echo ""
echo "4. Checking registration script..."
ls -la ../bug_reports/register_issue.py

echo ""
echo "5. To create a new issue, run:"
echo "   python3 ../bug_reports/register_issue.py"

echo ""
echo "The issue tracking system is ready to use!"