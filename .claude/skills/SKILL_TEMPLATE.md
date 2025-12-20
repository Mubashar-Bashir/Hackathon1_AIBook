# 🤖 AIDD Agent Skill Implementation Guide: skill_instructions.md

## 1. 🎯 Purpose and Philosophy

This document outlines the standard structure and required contents for every Agent IDD (AIDD) Skill. Following these guidelines ensures our skills are **composable, consistent, and maintainable**, leveraging Anthropic's core philosophy: **Don't Build Agents, Build Skills Instead.**

We aim to inject domain expertise and procedural knowledge into our general AIDD agents, making them reliable experts rather than merely brilliant generalists.

---

## 2. 📂 Skill Structure and File System (The "Folder")

A Skill is an **organized folder** that acts as the single source of truth for a specific capability.

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | **This file.** Contains the core instructions, usage guidelines, and the directory map for the agent. It is read upon skill *invocation*. | Progressive |
| `skill_metadata.json` | **Mandatory** | A small JSON file with a concise description and keywords for initial skill discovery. | Progressive (Initial) |
| `scripts/` | Optional | Contains all executable code (Python, Bash, etc.) the agent can use as a tool. | On Demand |
| `assets/` | Optional | Non-executable supporting files, e.g., templates, config files, reference CSVs, or binaries. | On Demand |
| `README.md` | Optional | Human-readable documentation for developers maintaining the skill. | Human Only |

---

## 3. 📄 `skill_metadata.json` Guidelines (Initial Disclosure)

This JSON file is mandatory and helps the agent decide if a skill is relevant **without** loading the full context.

| Key | Description | Example |
| :--- | :--- | :--- | :--- |
| `name` | Short, human-readable name. | "FinancialReportGenerator" |
| `version` | Semantic versioning (`major.minor.patch`). | "1.0.3" |
| `keywords` | Terms the agent will match to suggest the skill. | ["financial planning", "tax compliance", "IRS form 1040"] |
| `description` | **Concise summary (max 3 sentences)** of what the skill does. | "Analyzes raw transactional data, calculates tax liabilities, and generates a draft 1040-EZ form using internal best practices." |

---

## 4. 🧠 `skill_instructions.md` Content (The Core Expertise)

This file contains the precise procedural knowledge the agent needs to execute the task. It is the agent's **domain expertise injection**.

### A. Title and Description

* **Title:** Must clearly state the skill's action (e.g., "Generate Tax Report").
* **Context/Goal:** Clearly state *why* the skill exists (e.g., to ensure all tax reporting follows 2024 compliance standards).

### B. Procedural Steps (The "How")

* List the required steps in a clear, numbered format. This standardizes the agent's execution path, ensuring **consistency** over brilliance.
    1.  Check for required input files in `input/`.
    2.  Execute `scripts/tax_calculator.py` using the provided input data.
    3.  Compare the script output against validation rules specified in `assets/validation_rules.txt`.
    4.  Synthesize the final report using the required structure found in `assets/report_template.md`.
    5.  Save the final output as a `.docx` file in the `output/` directory, using the Document Skill if necessary.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Invocation:** Instruct the agent on how to use the scripts in the `scripts/` folder, including required arguments.
    * *Example Command:* `python scripts/data_analyzer.py --input $INPUT_FILE --year 2024`
* **Error Handling:** Include explicit instructions on what to do if a script fails.
    * *Guideline:* If a script returns an error, examine the log file in the runtime environment. If the error is persistent, try the **fallback script** located at `scripts/basic_analysis.sh` before escalating to the user.

### D. Inputs and Outputs

* **Inputs:**
    * Expected input format: A single CSV file named `transactions.csv`.
    * Required columns: `Date`, `Description`, `Amount`, `Category`.
* **Outputs:**
    * Expected output format: A Microsoft Word Document (`.docx`) for professional quality, named `[DATE]_Final_Compliance_Report.docx`.

---

## 5. 🛠️ Development & Maintenance (Treating Skills Like Software)

1.  **Versioning:** Always update the `version` in `skill_metadata.json` for non-trivial changes to maintain a clear **lineage** of agent behavior.
2.  **Testing:** Skills must be tested using the internal AIDD evaluation harness. Ensure the agent loads and triggers the skill at the correct time and that the output quality is measured against defined standards.
3.  **Dependencies:** If this skill relies on an external tool or server, explicitly document it.
    * *Example Dependency:* This skill requires access to the **FinancialDataMCP Server** for real-time market data lookups.