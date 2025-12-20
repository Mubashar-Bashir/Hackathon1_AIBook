# Educational Assessment Skill

## 1. 🎯 Purpose and Philosophy

This skill creates quizzes, exercises, and assessments for learning modules in the Physical AI & Humanoid Robotics textbook. It ensures assessments are pedagogically sound, appropriately challenging, and aligned with learning objectives.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for educational assessment creation | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for assessment generation | On Demand |
| `assets/` | Optional | Question templates, difficulty scales, and assessment rubrics | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Content Analysis**: Analyze the provided content or learning objectives to assess.
2.  **Difficulty Level Setting**: Determine appropriate difficulty based on education level.
3.  **Question Type Selection**: Choose appropriate question types (multiple choice, short answer, essay, practical).
4.  **Assessment Generation**: Create questions with correct answers and explanations.
5.  **Rubric Development**: Generate grading criteria and scoring guidelines.
6.  **Feedback Integration**: Include constructive feedback for each question.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/assessment_generator.py`
* **Invocation Command**: `python scripts/assessment_generator.py --topic "Physical AI concepts" --level "undergraduate" --question-count 10 --types "multiple-choice,short-answer"`
* **Configuration**: The script reads assessment templates from `assets/question_templates.json` which contains question patterns and difficulty guidelines.

### D. Inputs and Outputs

* **Inputs:**
    * `topic`: The subject matter to assess
    * `education_level`: Target education level (high school, undergraduate, graduate)
    * `question_count`: Number of questions to generate
    * `question_types`: Comma-separated list of question types
    * `learning_objectives`: Specific objectives to assess
* **Outputs:**
    * `questions`: Generated questions with answer choices and correct answers
    * `difficulty_levels`: Difficulty rating for each question
    * `grading_rubric`: Scoring guidelines for open-ended questions
    * `feedback`: Constructive feedback for each answer option

---

## 4. 🛠️ Error Handling

* **Insufficient Content**: If there's not enough content to generate the requested number of questions, generate what's possible and indicate the limitation.
* **Invalid Question Types**: If requested question types don't match the content, suggest appropriate alternatives.
* **Difficulty Mismatch**: If difficulty level doesn't match content complexity, adjust or warn about the mismatch.