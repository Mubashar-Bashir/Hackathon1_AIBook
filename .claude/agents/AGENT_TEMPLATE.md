# 🤖 AIDD Agent Implementation Guide: agent_instructions.md

## 1. 🎯 Purpose and Philosophy

This document outlines the standard structure and required contents for every Agent IDD (AIDD) Agent. Following these guidelines ensures our agents are **composable, consistent, and maintainable**, leveraging Anthropic's core philosophy: **Don't Build Monolithic Agents, Build Modular Agents Instead.**

We aim to create specialized agents that can operate within specific domains, with clear boundaries and well-defined interfaces to other components.

---

## 2. 📂 Agent Structure and File System (The "Folder")

An Agent is an **organized folder** that acts as the single source of truth for a specific agent capability.

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `agent_instructions.md` | **Mandatory** | **This file.** Contains the core instructions, role definition, and operational guidelines for the agent. It is read upon agent *initialization*. | Progressive |
| `agent_metadata.json` | **Mandatory** | A small JSON file with a concise description and keywords for initial agent discovery. | Progressive (Initial) |
| `skills/` | Optional | Contains references to or copies of skills this agent is authorized to use. | Progressive |
| `scripts/` | Optional | Contains all executable code (Python, Bash, etc.) the agent can execute as part of its operations. | On Demand |
| `assets/` | Optional | Non-executable supporting files, e.g., templates, config files, reference data. | On Demand |
| `README.md` | Optional | Human-readable documentation for developers maintaining the agent. | Human Only |

---

## 3. 📄 `agent_metadata.json` Guidelines (Initial Disclosure)

This JSON file is mandatory and helps the system decide if an agent is relevant **without** loading the full context.

| Key | Description | Example |
| :--- | :--- | :--- | :--- |
| `name` | Short, human-readable name. | "FinancialReportAgent" |
| `version` | Semantic versioning (`major.minor.patch`). | "1.0.3" |
| `keywords` | Terms the system will match to suggest the agent. | ["financial planning", "tax compliance", "report generation"] |
| `description` | **Concise summary (max 3 sentences)** of what the agent does. | "Specializes in analyzing financial data, calculating tax liabilities, and generating compliance reports using the FinancialReportGenerator skill." |
| `capabilities` | List of key capabilities the agent possesses. | ["data analysis", "report generation", "compliance checking"] |

---

## 4. 🧠 `agent_instructions.md` Content (The Core Identity)

This file contains the precise role definition, operational guidelines, and behavioral patterns the agent should follow. It is the agent's **core identity injection**.

### A. Title and Description

* **Title:** Must clearly state the agent's role (e.g., "Tax Compliance Agent").
* **Context/Goal:** Clearly state *why* the agent exists (e.g., to ensure all tax reporting follows 2024 compliance standards autonomously).

### B. Role Definition (The "Who")

* Define the agent's persona and core responsibilities in clear, actionable terms.
    1.  **Primary Role**: What is the agent's main function?
    2.  **Secondary Roles**: What other functions might the agent perform?
    3.  **Boundaries**: What is the agent NOT responsible for?

### C. Operational Guidelines (The "How")

* **Decision Making**: How should the agent approach problem-solving?
* **Interaction Patterns**: How should the agent interact with users or other systems?
* **Skill Selection**: How should the agent choose which skills to use?
* **Error Handling**: How should the agent respond to failures or unexpected situations?

### D. Capabilities and Limitations

* **Capabilities**: What can the agent do well?
* **Limitations**: What are the agent's boundaries and constraints?
* **Fallback Procedures**: What should the agent do when it encounters something beyond its capabilities?

---

## 5. 🛠️ Development & Maintenance (Treating Agents Like Software)

1.  **Versioning:** Always update the `version` in `agent_metadata.json` for non-trivial changes to maintain a clear **lineage** of agent behavior.
2.  **Testing:** Agents must be tested using the internal AIDD evaluation harness. Ensure the agent behaves appropriately across various scenarios and properly utilizes its authorized skills.
3.  **Dependencies:** If this agent relies on external services, tools, or other agents, explicitly document them.
    * *Example Dependency:* This agent requires access to the **FinancialDataMCP Server** and the **TaxCalculatorSkill**.