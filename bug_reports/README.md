# Issue Tracking and Resolution Process

This document outlines the process for reporting issues and registering their solutions in our system.

## Directory Structure

```
../bug_reports/
├── open/              # Currently open issues
├── closed/            # Issues that have been resolved
├── resolved/          # Solution documentation for resolved issues
├── metadata/          # Metadata and reports about issues
├── templates/         # Template files for standardization
└── register_issue.py  # Script for creating and registering issues
```

## Issue Reporting Process

### 1. Creating a New Issue
- Use the `register_issue.py` script to create standardized issue reports
- Run: `python3 ../bug_reports/register_issue.py` and select option 1
- Provide all required information as prompted
- Issues are created in the `open/` directory with a unique ID

### 2. Issue Status Flow
1. **Open**: New issues are placed in the `open/` directory
2. **In Progress**: Issues being actively worked on (status updated in issue file)
3. **Resolved**: Issues with solutions implemented and tested
4. **Closed**: Issues verified as resolved and moved to `closed/` directory

## Solution Registration Process

### 1. Registering a Solution
- Use the `register_issue.py` script to register solutions
- Run: `python3 ../bug_reports/register_issue.py` and select option 2
- Provide the Issue ID and solution details
- Solutions are stored in the `resolved/` directory

### 2. Automatic Issue Status Update
- When a solution is registered, the original issue is moved from `open/` to `closed/`
- The status in the original issue file is updated to "Resolved"

## Templates

### Issue Template
- Located at: `templates/issue_template.md`
- Provides standardized format for issue reports
- Ensures all necessary information is captured

### Solution Template
- Located at: `templates/solution_template.md`
- Provides standardized format for solution documentation
- Ensures proper root cause analysis and verification steps

## Metadata Tracking

### Issue Metadata Report
- Located at: `metadata/issue_metadata_report.md`
- Tracks overall issue statistics
- Provides summary information about all reported issues

## Best Practices

1. **Complete Information**: Fill out all relevant fields in the templates
2. **Descriptive Titles**: Use clear, specific titles for issues and solutions
3. **Reproducible Steps**: Provide detailed steps to reproduce issues
4. **Verification**: Always verify solutions before registering them
5. **Cross-Reference**: Link related issues when applicable
6. **Regular Updates**: Keep the metadata report updated regularly

## Issue ID Format

Issue IDs follow the format: `ISSUE-YYYYMMDD-XXXXXXXX`
- `YYYYMMDD`: Date when the issue was reported
- `XXXXXXXX`: Unique identifier (first 8 characters of UUID)

## Example Workflow

1. Developer encounters a bug
2. Runs `python3 ../bug_reports/register_issue.py` to create issue report
3. Works on fixing the bug
4. Once fixed and tested, runs script again to register solution
5. System automatically moves original issue to closed and creates solution documentation
6. Updates metadata report with new information

## Script Usage

```bash
# To create/register issues:
python3 ../bug_reports/register_issue.py

# The script provides an interactive menu for:
# 1. Creating new issue reports
# 2. Registering solutions for existing issues
```

## File Naming Convention

- Issue files: `ISSUE-YYYYMMDD-XXXX_Title.md`
- Solution files: `SOLUTION_ISSUE-YYYYMMDD-XXXX_Title.md`

This system ensures consistent tracking and documentation of all issues and their resolutions.