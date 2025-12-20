# Translation Management Skill

## 1. 🎯 Purpose and Philosophy

This skill manages multilingual content for the Physical AI & Humanoid Robotics textbook, handling translation workflows, locale management, and cultural adaptation to ensure global accessibility and inclusive learning experiences.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for translation management | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for translation processing and management | On Demand |
| `assets/` | Optional | Translation memories, locale configurations, and cultural guidelines | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Content Analysis**: Analyze source content for translatable elements.
2.  **Locale Identification**: Identify target locales and cultural considerations.
3.  **Translation Workflow**: Manage the translation process from source to target.
4.  **Quality Assurance**: Ensure translation accuracy and cultural appropriateness.
5.  **Integration Management**: Integrate translations into the application.
6.  **Cultural Adaptation**: Adapt content for cultural relevance and sensitivity.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/translation_manager.py`
* **Invocation Command**: `python scripts/translation_manager.py --source "en" --target "ur" --content-path "./book/docs" --workflow "automated-review"`
* **Configuration**: The script reads locale settings from `assets/locale_config.json` which contains language-specific settings and cultural guidelines.

### D. Inputs and Outputs

* **Inputs:**
    * `source`: Source language code (e.g., en, es, fr)
    * `target`: Target language code (e.g., ur, es, fr)
    * `content_path`: Path to content that needs translation
    * `workflow`: Translation workflow (automated, human-reviewed, hybrid)
* **Outputs:**
    * `translated_content`: Content in the target language
    * `translation_quality`: Quality score and issues found
    * `cultural_adaptations`: Cultural considerations applied
    * `integration_report`: Report on translation integration status

---

## 4. 🛠️ Error Handling

* **Unsupported Language**: If the target language is not supported, return available language options.
* **Content Format Issues**: If content cannot be parsed for translation, return specific error details.
* **Quality Threshold**: If translation quality falls below acceptable levels, flag for human review.