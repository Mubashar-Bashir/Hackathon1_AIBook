# Security Audit Skill

## 1. 🎯 Purpose and Philosophy

This skill performs security analysis of the Physical AI & Humanoid Robotics textbook application, identifying vulnerabilities and ensuring security best practices are followed to protect user data and system integrity.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for security auditing | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for vulnerability scanning and security analysis | On Demand |
| `assets/` | Optional | Security checklists, vulnerability databases, and compliance standards | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Code Analysis**: Analyze source code for common security vulnerabilities.
2.  **Dependency Check**: Scan dependencies for known vulnerabilities.
3.  **Configuration Review**: Review configuration files for security misconfigurations.
4.  **Vulnerability Identification**: Identify specific security issues and their severity.
5.  **Compliance Check**: Verify adherence to security standards and best practices.
6.  **Remediation Guidance**: Provide specific steps to address identified issues.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/security_scanner.py`
* **Invocation Command**: `python scripts/security_scanner.py --project-path "./backend" --check-types "sast,dependencies,config"`
* **Configuration**: The script reads security patterns from `assets/security_patterns.json` which contains vulnerability signatures and security best practices.

### D. Inputs and Outputs

* **Inputs:**
    * `project_path`: Path to the project to analyze
    * `check_types`: Comma-separated list of check types (sast, dependencies, config)
    * `severity_threshold`: Minimum severity level to report (low, medium, high, critical)
    * `compliance_standard`: Security standard to check against (OWASP, NIST, etc.)
* **Outputs:**
    * `vulnerabilities`: Identified security vulnerabilities with details
    * `risk_assessment`: Risk level for each vulnerability
    * `remediation_steps`: Specific steps to fix each issue
    * `compliance_status`: Compliance with security standards

---

## 4. 🛠️ Error Handling

* **Inaccessible Project**: If the project path is invalid or inaccessible, return an error message.
* **Analysis Failure**: If security analysis cannot be completed, provide specific error details.
* **Unknown Vulnerability**: If a potential issue is detected but cannot be classified, flag for expert review.