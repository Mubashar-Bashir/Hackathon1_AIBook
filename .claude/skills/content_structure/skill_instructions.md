# Content Structure Skill

## 1. 🎯 Purpose and Philosophy

This skill helps organize textbook content into proper learning modules with appropriate structure, learning objectives, and pedagogical flow. It ensures the Physical AI & Humanoid Robotics textbook follows best practices for educational content organization.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for content structure organization | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for content analysis and structuring | On Demand |
| `assets/` | Optional | Educational frameworks, learning objectives templates, and content patterns | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Content Analysis**: Analyze the provided content or topic for educational structure needs.
2.  **Learning Objective Setting**: Define clear, measurable learning objectives for the module.
3.  **Structure Planning**: Organize content into appropriate sections with logical flow.
4.  **Pedagogical Alignment**: Ensure content follows established educational principles.
5.  **Assessment Integration**: Plan for formative and summative assessments.
6.  **Accessibility Consideration**: Structure content for diverse learning needs.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/content_structure_analyzer.py`
* **Invocation Command**: `python scripts/content_structure_analyzer.py --topic "Physical AI foundations" --level "undergraduate" --sections 5`
* **Configuration**: The script reads educational frameworks from `assets/learning_frameworks.json` which contains Bloom's taxonomy levels and pedagogical patterns.

### D. Inputs and Outputs

* **Inputs:**
    * `topic`: The subject matter to structure
    * `education_level`: Target education level (high school, undergraduate, graduate)
    * `sections`: Number of sections or chapters desired
    * `learning_objectives`: Specific objectives to address
* **Outputs:**
    * `structure`: Proposed content structure with sections and subsections
    * `objectives`: Learning objectives for each section
    * `activities`: Suggested learning activities
    * `assessments`: Recommended assessment methods

---

## 4. 🛠️ Error Handling

* **Unclear Topic**: If the topic is too broad or vague, request clarification or suggest focus areas.
* **Conflicting Objectives**: If learning objectives conflict with content, suggest adjustments.
* **Structural Issues**: If proposed structure doesn't align with pedagogical best practices, suggest alternatives.