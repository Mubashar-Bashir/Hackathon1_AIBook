#!/usr/bin/env python3
"""
Issue and Solution Registration System
This script helps create standardized issue reports and solution registrations.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import uuid

def create_issue_report():
    """Create a new issue report using the template."""
    print("Creating a new issue report...")

    # Collect basic information
    title = input("Issue Title: ").strip()
    description = input("Description: ").strip()

    # Generate unique ID
    issue_id = f"ISSUE-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

    # Select priority
    priorities = ["Low", "Medium", "High", "Critical"]
    print("\nSelect Priority:")
    for i, priority in enumerate(priorities, 1):
        print(f"{i}. {priority}")
    priority_choice = int(input("Enter choice (1-4): ")) - 1
    priority = priorities[priority_choice]

    # Select severity
    severities = ["Trivial", "Minor", "Major", "Critical", "Blocker"]
    print("\nSelect Severity:")
    for i, severity in enumerate(severities, 1):
        print(f"{i}. {severity}")
    severity_choice = int(input("Enter choice (1-5): ")) - 1
    severity = severities[severity_choice]

    # Get environment details
    version = input("Software Version: ").strip()
    platform = input("Platform (OS/Browser): ").strip()
    environment = input("Environment (Dev/Staging/Prod): ").strip()

    # Create the issue report content
    issue_content = f"""# Issue Report: {title}

## Basic Information
- **Issue ID**: {issue_id}
- **Title**: {title}
- **Reported Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Reported By**: [Your Name]
- **Priority**: {priority}
- **Severity**: {severity}
- **Status**: Open

## Environment Details
- **Version**: {version}
- **Platform**: {platform}
- **Environment**: {environment}

## Description
{description}

## Steps to Reproduce
1.
2.
3.
4. ...

## Actual Result


## Expected Result


## Screenshots/Logs


## Additional Information


## Tags
[Labels: e.g., bug, enhancement, documentation, security, performance]
"""

    # Save the issue report
    issue_filename = f"{issue_id}_{title.replace(' ', '_').replace('/', '_')}.md"
    issue_path = Path("../bug_reports/open") / issue_filename

    with open(issue_path, 'w', encoding='utf-8') as f:
        f.write(issue_content)

    print(f"\nIssue report created: {issue_path}")
    return str(issue_path)

def register_solution():
    """Register a solution for an existing issue."""
    print("Registering a solution for an issue...")

    issue_id = input("Issue ID (e.g., ISSUE-20251219-ABCDEF12): ").strip()
    solution_title = input("Solution Title: ").strip()

    # Select resolution status
    statuses = ["Fixed", "Won't Fix", "Duplicate", "Not Reproducible", "Works as Expected"]
    print("\nSelect Resolution Status:")
    for i, status in enumerate(statuses, 1):
        print(f"{i}. {status}")
    status_choice = int(input("Enter choice (1-5): ")) - 1
    resolution_status = statuses[status_choice]

    # Get solution details
    root_cause = input("Root Cause Analysis: ").strip()
    solution_desc = input("Solution Description: ").strip()

    # Create the solution registration content
    solution_content = f"""# Solution Registration: {solution_title}

## Resolution Information
- **Issue ID**: {issue_id}
- **Solution Title**: {solution_title}
- **Resolution Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Resolved By**: [Your Name]
- **Resolution Status**: {resolution_status}

## Root Cause Analysis
{root_cause}

## Solution Description
{solution_desc}

## Changes Made
- [Change 1]
- [Change 2]
- [Change 3]
- ...

## Files Modified


## Testing Performed


## Verification Steps


## Rollback Plan


## Related Issues


## Approval
- **Reviewed By**: [Name]
- **Approved Date**: {datetime.now().strftime('%Y-%m-%d')}

## Additional Notes

"""

    # Save the solution registration
    solution_filename = f"SOLUTION_{issue_id}_{solution_title.replace(' ', '_').replace('/', '_')}.md"
    solution_path = Path("../bug_reports/resolved") / solution_filename

    with open(solution_path, 'w', encoding='utf-8') as f:
        f.write(solution_content)

    # Move the original issue to closed folder
    original_issue_path = None
    for status_dir in ['open', 'closed']:
        potential_path = Path(f"../bug_reports/{status_dir}/{issue_id}_*.md")
        for path in Path(f"../bug_reports/{status_dir}").glob(f"{issue_id}_*.md"):
            original_issue_path = path
            break
        if original_issue_path:
            break

    if original_issue_path:
        # Update the status in the original issue file
        with open(original_issue_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace the status line
        content = content.replace("- **Status**: Open", f"- **Status**: Resolved")

        # Move to closed folder
        closed_path = Path("../bug_reports/closed") / original_issue_path.name
        os.rename(original_issue_path, closed_path)
        print(f"Original issue moved to closed: {closed_path}")

    print(f"\nSolution registration created: {solution_path}")
    return str(solution_path)

def main():
    print("Issue and Solution Registration System")
    print("=" * 40)
    print("1. Create new issue report")
    print("2. Register solution for existing issue")
    print("3. Exit")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        create_issue_report()
    elif choice == "2":
        register_solution()
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        main()

if __name__ == "__main__":
    # Ensure the required directories exist
    os.makedirs("../bug_reports/open", exist_ok=True)
    os.makedirs("../bug_reports/closed", exist_ok=True)
    os.makedirs("../bug_reports/resolved", exist_ok=True)
    os.makedirs("../bug_reports/metadata", exist_ok=True)
    os.makedirs("../bug_reports/templates", exist_ok=True)

    main()