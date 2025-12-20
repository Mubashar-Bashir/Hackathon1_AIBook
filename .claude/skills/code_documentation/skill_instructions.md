# Code Documentation Skill

## 1. 🎯 Purpose and Philosophy

This skill generates comprehensive documentation for codebases, including API documentation, code comments, and usage examples. It ensures the Physical AI & Humanoid Robotics textbook project code is well-documented and maintainable.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for code documentation generation | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for documentation generation and analysis | On Demand |
| `assets/` | Optional | Documentation templates, style guides, and best practices | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Code Analysis**: Analyze the provided code to identify functions, classes, parameters, and return values.
2.  **Documentation Template Selection**: Choose appropriate documentation templates based on code type and language.
3.  **Content Generation**: Create clear, concise documentation with examples.
4.  **Style Consistency**: Apply consistent formatting and style according to project standards.
5.  **Example Creation**: Generate usage examples that demonstrate proper implementation.
6.  **Quality Review**: Ensure documentation is accurate, complete, and helpful.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/documentation_generator.py`
* **Invocation Command**: `python scripts/documentation_generator.py --code "function_code" --language "python" --format "markdown"`
* **Configuration**: The script reads documentation templates from `assets/doc_templates.json` which contains language-specific templates and style guidelines.

### D. Inputs and Outputs

* **Inputs:**
    * `code`: The source code to document
    * `language`: Programming language of the code (python, javascript, typescript, etc.)
    * `format`: Output format (markdown, html, json, etc.)
    * `include_examples`: Whether to include usage examples
* **Outputs:**
    * `documentation`: Generated documentation content
    * `api_reference`: Structured API reference
    * `usage_examples`: Code examples demonstrating usage
    * `style_compliance`: Report on documentation style compliance

---

## 4. 🛠️ Error Handling

* **Unsupported Language**: If the code language is not supported, return available language options.
* **Invalid Code**: If the code cannot be parsed, return an error message with suggestions.
* **Incomplete Information**: If required information is missing, flag for manual review.