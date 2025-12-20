#!/usr/bin/env python3
"""
Accessibility Checker Script

This script evaluates UI components and interfaces for accessibility compliance according to WCAG 2.1 standards.
"""

import argparse
import json
import os
import re
from typing import Dict, List, Any, Tuple

def load_wcag_guidelines():
    """Load WCAG guidelines from assets/wcag_guidelines.json"""
    guidelines_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'wcag_guidelines.json')
    if os.path.exists(guidelines_path):
        with open(guidelines_path, 'r') as f:
            return json.load(f)
    else:
        # Default WCAG guidelines
        return {
            "levels": {
                "A": "Minimum level of conformance",
                "AA": "Balanced level of conformance",
                "AAA": "Highest level of conformance"
            },
            "principles": {
                "Perceivable": {
                    "guidelines": [
                        {
                            "id": "1.1.1",
                            "title": "Non-text Content",
                            "level": "A",
                            "description": "All non-text content has text alternatives"
                        },
                        {
                            "id": "1.2.1",
                            "title": "Audio-only and Video-only (Prerecorded)",
                            "level": "A",
                            "description": "Provide alternatives for time-based media"
                        },
                        {
                            "id": "1.3.1",
                            "title": "Info and Relationships",
                            "level": "A",
                            "description": "Information is programmatically determinable"
                        },
                        {
                            "id": "1.4.3",
                            "title": "Contrast (Minimum)",
                            "level": "AA",
                            "description": "Visual presentation has sufficient contrast ratio"
                        },
                        {
                            "id": "1.4.4",
                            "title": "Resize text",
                            "level": "AA",
                            "description": "Text can be resized without assistive technology"
                        }
                    ]
                },
                "Operable": {
                    "guidelines": [
                        {
                            "id": "2.1.1",
                            "title": "Keyboard",
                            "level": "A",
                            "description": "Functionality is operable from keyboard"
                        },
                        {
                            "id": "2.4.7",
                            "title": "Focus Visible",
                            "level": "AA",
                            "description": "Focus indicator is visible"
                        }
                    ]
                },
                "Understandable": {
                    "guidelines": [
                        {
                            "id": "3.1.1",
                            "title": "Language of Page",
                            "level": "A",
                            "description": "Default human language is identified"
                        }
                    ]
                },
                "Robust": {
                    "guidelines": [
                        {
                            "id": "4.1.2",
                            "title": "Name, Role, Value",
                            "level": "A",
                            "description": "Elements have complete accessibility information"
                        }
                    ]
                }
            }
        }

def check_accessibility_issues(code: str) -> List[Dict[str, Any]]:
    """Check code for accessibility issues."""
    issues = []

    # Check for missing alt attributes in images
    img_pattern = r'<img(?![^>]*alt=)[^>]*>'
    img_matches = re.findall(img_pattern, code, re.IGNORECASE)
    if img_matches:
        issues.append({
            "id": "img-missing-alt",
            "severity": "critical",
            "description": "Image elements missing alt attributes",
            "count": len(img_matches),
            "wcag_guidelines": ["1.1.1"],
            "recommendation": "Add descriptive alt text to all img elements, or use empty alt for decorative images",
            "code_snippets": img_matches[:3]  # Limit to first 3 snippets
        })

    # Check for missing labels for form elements
    label_pattern = r'<(input|select|textarea)(?![^>]*id=)(?![^>]*aria-label=)(?![^>]*aria-labelledby=)[^>]*>'
    label_matches = re.findall(label_pattern, code, re.IGNORECASE)
    if label_matches:
        issues.append({
            "id": "form-element-missing-label",
            "severity": "high",
            "description": "Form elements missing associated labels",
            "count": len(label_matches),
            "wcag_guidelines": ["1.3.1", "4.1.2"],
            "recommendation": "Associate form elements with labels using for/id attributes, aria-label, or aria-labelledby",
            "code_snippets": label_matches[:3]
        })

    # Check for insufficient color contrast
    style_pattern = r'(?:color|background-color|background):\s*([^;}]*)'
    color_matches = re.findall(style_pattern, code, re.IGNORECASE)
    if color_matches:
        # This is a simplified check - in reality, you'd need to parse actual color values
        issues.append({
            "id": "potential-contrast-issue",
            "severity": "medium",
            "description": "Potential color contrast issues detected - verify against WCAG standards",
            "count": len(color_matches),
            "wcag_guidelines": ["1.4.3"],
            "recommendation": "Ensure text has sufficient contrast ratio (4.5:1 for normal text, 3:1 for large text)",
            "code_snippets": color_matches[:3]
        })

    # Check for missing focus indicators
    focus_pattern = r':focus\s*{[^}]*outline:\s*none'
    focus_matches = re.findall(focus_pattern, code, re.IGNORECASE)
    if focus_matches:
        issues.append({
            "id": "focus-indicator-removed",
            "severity": "high",
            "description": "Focus indicators removed without replacement",
            "count": len(focus_matches),
            "wcag_guidelines": ["2.4.7"],
            "recommendation": "Provide visible focus indicators for keyboard navigation, using outline or other visual cues",
            "code_snippets": focus_matches[:3]
        })

    # Check for missing ARIA attributes where needed
    button_pattern = r'<button(?![^>]*(aria-label|aria-labelledby|title))[^>]*>'
    button_matches = re.findall(button_pattern, code, re.IGNORECASE)
    if button_matches:
        issues.append({
            "id": "button-missing-accessibility-label",
            "severity": "medium",
            "description": "Buttons missing accessibility labels",
            "count": len(button_matches),
            "wcag_guidelines": ["4.1.2"],
            "recommendation": "Add aria-label, aria-labelledby, or title to buttons without visible text",
            "code_snippets": button_matches[:3]
        })

    # Check for missing language declaration
    lang_pattern = r'<html(?![^>]*lang=)'
    lang_matches = re.findall(lang_pattern, code, re.IGNORECASE)
    if lang_matches:
        issues.append({
            "id": "missing-language-declaration",
            "severity": "medium",
            "description": "HTML element missing language declaration",
            "count": len(lang_matches),
            "wcag_guidelines": ["3.1.1"],
            "recommendation": "Add lang attribute to the html element (e.g., <html lang='en'>)",
            "code_snippets": lang_matches[:3]
        })

    return issues

def calculate_compliance_score(issues: List[Dict[str, Any]]) -> float:
    """Calculate an overall accessibility compliance score."""
    if not issues:
        return 100.0

    # Weighted scoring based on severity
    severity_weights = {
        "critical": 10,
        "high": 5,
        "medium": 2,
        "low": 1
    }

    total_deduction = 0
    for issue in issues:
        severity = issue.get("severity", "medium")
        count = issue.get("count", 1)
        weight = severity_weights.get(severity, 2)
        total_deduction += count * weight

    # Calculate score (higher deduction = lower score)
    score = max(0, 100 - min(total_deduction, 95))
    return round(score, 2)

def main():
    parser = argparse.ArgumentParser(description='Accessibility Checker')
    parser.add_argument('--input', type=str, required=True, help='Code or HTML to analyze for accessibility')
    parser.add_argument('--level', type=str, default='AA', choices=['A', 'AA', 'AAA'], help='WCAG compliance level')

    args = parser.parse_args()

    # Check for accessibility issues
    issues = check_accessibility_issues(args.input)

    # Calculate compliance score
    compliance_score = calculate_compliance_score(issues)

    # Prepare output
    output = {
        "input_type": "code",
        "wcag_level": args.level,
        "issues": issues,
        "total_issues": len(issues),
        "compliance_score": compliance_score,
        "summary": {
            "critical": len([i for i in issues if i["severity"] == "critical"]),
            "high": len([i for i in issues if i["severity"] == "high"]),
            "medium": len([i for i in issues if i["severity"] == "medium"]),
            "low": len([i for i in issues if i["severity"] == "low"])
        }
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()