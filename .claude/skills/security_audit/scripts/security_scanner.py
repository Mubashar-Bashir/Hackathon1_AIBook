#!/usr/bin/env python3
"""
Security Scanner Script

This script performs security analysis of the Physical AI & Humanoid Robotics textbook application,
identifying vulnerabilities and ensuring security best practices are followed.
"""

import argparse
import json
import os
import re
from typing import Dict, List, Any

def load_security_patterns():
    """Load security patterns from assets/security_patterns.json"""
    patterns_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'security_patterns.json')
    if os.path.exists(patterns_path):
        with open(patterns_path, 'r') as f:
            return json.load(f)
    else:
        # Default security patterns
        return {
            "sast_patterns": {
                "injection": {
                    "patterns": [
                        r'cursor\.execute\([^)]*[\+\%]\s*.*\)',
                        r'os\.system\([^)]*[\+\%]\s*.*\)',
                        r'eval\([^)]*[\+\%]\s*.*\)',
                        r'exec\([^)]*[\+\%]\s*.*\)',
                        r'subprocess\.(call|run|Popen)\([^)]*[\+\%]\s*.*\)'
                    ],
                    "severity": "critical",
                    "description": "Potential code/command injection vulnerability"
                },
                "xss": {
                    "patterns": [
                        r'return.*render.*[^<]*{[^}]*}[^>]*',
                        r'html\s*=\s*.*\+.*\+.*',
                        r'dangerouslySetInnerHTML'
                    ],
                    "severity": "high",
                    "description": "Potential cross-site scripting vulnerability"
                },
                "hardcoded_secrets": {
                    "patterns": [
                        r'password\s*[:=]\s*["\'][^"\']+["\']',
                        r'api_key\s*[:=]\s*["\'][^"\']+["\']',
                        r'secret\s*[:=]\s*["\'][^"\']+["\']',
                        r'token\s*[:=]\s*["\'][^"\']+["\']',
                        r'AWS_ACCESS_KEY_ID.*=.*["\'][A-Z0-9]+["\']',
                        r'AWS_SECRET_ACCESS_KEY.*=.*["\'][A-Za-z0-9/+=]+["\']'
                    ],
                    "severity": "high",
                    "description": "Hardcoded secret detected"
                },
                "path_traversal": {
                    "patterns": [
                        r'open\([^)]*[\+\%]\s*.*\)',
                        r'os\.path\.join\([^)]*[\+\%]\s*.*\)',
                        r'file\s*=\s*request\.args\['
                    ],
                    "severity": "high",
                    "description": "Potential path traversal vulnerability"
                }
            },
            "config_issues": {
                "debug_enabled": {
                    "patterns": [
                        r'DEBUG\s*[:=]\s*True',
                        r'debug\s*[:=]\s*true',
                        r'--debug',
                        r'--dev'
                    ],
                    "severity": "medium",
                    "description": "Debug mode enabled in production"
                },
                "cors_misconfig": {
                    "patterns": [
                        r'Access-Control-Allow-Origin\s*[:=]\s*["\']\*["\']',
                        r'allow_origins=\["\*\"]'
                    ],
                    "severity": "medium",
                    "description": "CORS configured to allow all origins"
                }
            },
            "security_best_practices": [
                "Use parameterized queries to prevent SQL injection",
                "Validate and sanitize all user inputs",
                "Implement proper authentication and authorization",
                "Use HTTPS for all communications",
                "Store secrets securely using environment variables or secret management systems",
                "Implement proper error handling without exposing system details",
                "Use secure session management",
                "Apply principle of least privilege",
                "Keep dependencies up to date",
                "Perform regular security audits"
            ]
        }

def scan_file_for_vulnerabilities(file_path: str, patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Scan a file for security vulnerabilities based on patterns."""

    vulnerabilities = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        # Check for SAST patterns
        for vuln_type, vuln_info in patterns["sast_patterns"].items():
            for pattern in vuln_info["patterns"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Find the line number
                    line_no = content[:match.start()].count('\n') + 1
                    line_content = lines[line_no - 1] if line_no <= len(lines) else ""

                    vulnerabilities.append({
                        "type": vuln_type,
                        "severity": vuln_info["severity"],
                        "description": vuln_info["description"],
                        "file": file_path,
                        "line": line_no,
                        "code_snippet": line_content.strip(),
                        "pattern_matched": match.group(0)
                    })

        # Check for configuration issues
        for config_type, config_info in patterns["config_issues"].items():
            for pattern in config_info["patterns"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_no = content[:match.start()].count('\n') + 1
                    line_content = lines[line_no - 1] if line_no <= len(lines) else ""

                    vulnerabilities.append({
                        "type": config_type,
                        "severity": config_info["severity"],
                        "description": config_info["description"],
                        "file": file_path,
                        "line": line_no,
                        "code_snippet": line_content.strip(),
                        "pattern_matched": match.group(0)
                    })

    except Exception as e:
        print(f"Error scanning file {file_path}: {str(e)}")

    return vulnerabilities

def analyze_project_security(project_path: str) -> Dict[str, Any]:
    """Analyze the project for security vulnerabilities."""

    patterns = load_security_patterns()
    all_vulnerabilities = []

    # Walk through all files in the project
    for root, dirs, files in os.walk(project_path):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv', '.venv', '.next', 'dist', 'build']]

        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.htm', '.json', '.yaml', '.yml', '.xml', '.config')):
                file_path = os.path.join(root, file)
                vulnerabilities = scan_file_for_vulnerabilities(file_path, patterns)
                all_vulnerabilities.extend(vulnerabilities)

    return {
        "project_path": project_path,
        "total_vulnerabilities": len(all_vulnerabilities),
        "vulnerabilities": all_vulnerabilities,
        "by_severity": {
            "critical": len([v for v in all_vulnerabilities if v["severity"] == "critical"]),
            "high": len([v for v in all_vulnerabilities if v["severity"] == "high"]),
            "medium": len([v for v in all_vulnerabilities if v["severity"] == "medium"]),
            "low": len([v for v in all_vulnerabilities if v["severity"] == "low"])
        }
    }

def generate_remediation_guidance(vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate remediation guidance for identified vulnerabilities."""

    remediation_guidance = []

    for vuln in vulnerabilities:
        guidance = {
            "vulnerability_id": f"{vuln['type']}_{vuln['file']}_{vuln['line']}",
            "type": vuln["type"],
            "severity": vuln["severity"],
            "location": f"{vuln['file']}:{vuln['line']}",
            "issue": vuln["description"],
            "recommendation": "",
            "references": []
        }

        # Provide specific recommendations based on vulnerability type
        if vuln["type"] == "injection":
            guidance["recommendation"] = "Use parameterized queries or prepared statements. Validate and sanitize all inputs."
            guidance["references"] = [
                "https://owasp.org/www-community/attacks/Code_Injection",
                "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
            ]
        elif vuln["type"] == "xss":
            guidance["recommendation"] = "Escape all user inputs before rendering. Use built-in XSS protection features."
            guidance["references"] = [
                "https://owasp.org/www-community/attacks/xss/",
                "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
            ]
        elif vuln["type"] == "hardcoded_secrets":
            guidance["recommendation"] = "Move secrets to environment variables or a secure secret management system. Never commit secrets to version control."
            guidance["references"] = [
                "https://owasp.org/www-project-proactive-controls/v3/en/c6-configure-management",
                "https://12factor.net/config"
            ]
        elif vuln["type"] == "path_traversal":
            guidance["recommendation"] = "Validate file paths and use allowlists for allowed file extensions. Never directly use user input in file paths."
            guidance["references"] = [
                "https://owasp.org/www-community/attacks/Path_Traversal",
                "https://cheatsheetseries.owasp.org/cheatsheets/Path_Traversal_Prevention_Cheat_Sheet.html"
            ]
        elif vuln["type"] == "debug_enabled":
            guidance["recommendation"] = "Disable debug mode in production environments. Use environment-specific configurations."
            guidance["references"] = [
                "https://owasp.org/www-project-top-ten/2017/A03_2017-Sensitive_Data_Exposure"
            ]
        elif vuln["type"] == "cors_misconfig":
            guidance["recommendation"] = "Specify exact allowed origins instead of wildcard. Implement proper CORS policies."
            guidance["references"] = [
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS",
                "https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/02-Test_Cross_Origin_Resource_Sharing"
            ]

        remediation_guidance.append(guidance)

    return remediation_guidance

def main():
    parser = argparse.ArgumentParser(description='Security Scanner')
    parser.add_argument('--project-path', type=str, required=True, help='Path to the project to analyze')
    parser.add_argument('--check-types', type=str, default='sast,dependencies,config',
                       help='Comma-separated list of check types')
    parser.add_argument('--severity-threshold', type=str, default='low',
                       choices=['low', 'medium', 'high', 'critical'],
                       help='Minimum severity level to report')
    parser.add_argument('--compliance-standard', type=str, default='OWASP',
                       choices=['OWASP', 'NIST', 'ISO27001'],
                       help='Security standard to check against')

    args = parser.parse_args()

    # Validate project path
    if not os.path.exists(args.project_path):
        print(json.dumps({
            "error": f"Project path does not exist: {args.project_path}"
        }))
        return

    # Analyze project security
    security_analysis = analyze_project_security(args.project_path)

    # Generate remediation guidance
    remediation_guidance = generate_remediation_guidance(security_analysis["vulnerabilities"])

    # Filter by severity threshold
    severity_map = {
        'critical': 4,
        'high': 3,
        'medium': 2,
        'low': 1
    }
    threshold_level = severity_map[args.severity_threshold]

    filtered_vulnerabilities = []
    filtered_guidance = []

    for vuln in security_analysis["vulnerabilities"]:
        vuln_level = severity_map[vuln["severity"]]
        if vuln_level >= threshold_level:
            filtered_vulnerabilities.append(vuln)

    for guide in remediation_guidance:
        guide_level = severity_map[guide["severity"]]
        if guide_level >= threshold_level:
            filtered_guidance.append(guide)

    # Prepare output
    output = {
        "input": {
            "project_path": args.project_path,
            "check_types": args.check_types.split(','),
            "severity_threshold": args.severity_threshold,
            "compliance_standard": args.compliance_standard
        },
        "analysis": {
            "total_vulnerabilities": len(filtered_vulnerabilities),
            "vulnerabilities": filtered_vulnerabilities,
            "by_severity": {
                "critical": len([v for v in filtered_vulnerabilities if v["severity"] == "critical"]),
                "high": len([v for v in filtered_vulnerabilities if v["severity"] == "high"]),
                "medium": len([v for v in filtered_vulnerabilities if v["severity"] == "medium"]),
                "low": len([v for v in filtered_vulnerabilities if v["severity"] == "low"])
            }
        },
        "remediation": filtered_guidance,
        "compliance": {
            "standard": args.compliance_standard,
            "best_practices_followed": len([v for v in filtered_vulnerabilities if v["severity"] in ["high", "critical"]]) == 0,
            "recommendations": load_security_patterns()["security_best_practices"]
        }
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()