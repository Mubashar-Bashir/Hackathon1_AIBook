# Accessibility Checker Skill

## 1. 🎯 Purpose and Philosophy

This skill evaluates UI components and interfaces for accessibility compliance according to WCAG 2.1 standards. It ensures that the Physical AI & Humanoid Robotics textbook is usable by people with diverse abilities and disabilities.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for accessibility checking | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for accessibility analysis | On Demand |
| `assets/` | Optional | WCAG guidelines, checklists, and configurations | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Content Analysis**: Analyze the provided code, design, or interface for accessibility issues.
2.  **WCAG Compliance Check**: Evaluate against WCAG 2.1 AA standards (and AAA where applicable).
3.  **Issue Identification**: Identify specific accessibility violations and their severity levels.
4.  **Recommendation Generation**: Provide specific, actionable recommendations for fixes.
5.  **Prioritization**: Rank issues by impact and ease of implementation.
6.  **Documentation**: Create accessibility reports and remediation guides.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/accessibility_checker.py`
* **Invocation Command**: `python scripts/accessibility_checker.py --input "component_code" --level "AA"`
* **Configuration**: The script reads WCAG guidelines from `assets/wcag_guidelines.json` which contains success criteria and techniques.

### D. Inputs and Outputs

* **Inputs:**
    * `input`: The code, design, or interface to analyze
    * `level`: WCAG compliance level (A, AA, AAA)
    * `context`: Additional context about the component or page
* **Outputs:**
    * `issues`: List of identified accessibility issues
    * `severity`: Severity level of each issue (critical, high, medium, low)
    * `recommendations`: Specific recommendations for fixing issues
    * `compliance_score`: Overall accessibility compliance percentage

---

## 4. 🛠️ Error Handling

* **Invalid Input**: If the input format is not recognized, return available input formats.
* **Complex Issues**: If issues require specialized knowledge, flag for expert review.
* **False Positives**: Allow for manual override of flagged items that are not actual issues.