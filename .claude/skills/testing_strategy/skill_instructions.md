# Testing Strategy Skill

## 1. 🎯 Purpose and Philosophy

This skill creates comprehensive testing plans and strategies for the Physical AI & Humanoid Robotics textbook project, ensuring code quality and reliability through systematic testing approaches that cover all aspects of the application.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for testing strategy creation | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for test generation and coverage analysis | On Demand |
| `assets/` | Optional | Test templates, coverage standards, and quality metrics | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Project Analysis**: Analyze the project structure to identify testable components.
2.  **Test Strategy Planning**: Create a comprehensive testing strategy based on project architecture.
3.  **Test Type Selection**: Determine appropriate test types (unit, integration, e2e) for each component.
4.  **Test Generation**: Generate test cases based on functionality and requirements.
5.  **Coverage Analysis**: Define coverage targets and measurement approaches.
6.  **Quality Assurance**: Establish quality metrics and validation criteria.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/test_strategy_generator.py`
* **Invocation Command**: `python scripts/test_strategy_generator.py --project-path "./backend" --coverage-target 80 --test-types "unit,integration,e2e"`
* **Configuration**: The script reads testing standards from `assets/testing_standards.json` which contains best practices and quality metrics.

### D. Inputs and Outputs

* **Inputs:**
    * `project_path`: Path to the project to analyze
    * `coverage_target`: Desired test coverage percentage
    * `test_types`: Comma-separated list of test types to generate
    * `architecture`: Project architecture pattern (MVC, MVVM, etc.)
* **Outputs:**
    * `test_plan`: Comprehensive testing plan with test cases
    * `coverage_strategy`: Strategy for achieving coverage targets
    * `quality_metrics`: Defined quality metrics and thresholds
    * `test_automation`: Recommendations for test automation

---

## 4. 🛠️ Error Handling

* **Inaccessible Project**: If the project path is invalid or inaccessible, return an error message.
* **Unsupported Architecture**: If the architecture is not recognized, use general best practices.
* **Analysis Failure**: If test analysis cannot be completed, provide specific error details.