# Content Navigation Skill

## 1. 🎯 Purpose and Philosophy

This skill enables navigation and location of specific content within the Physical AI & Humanoid Robotics textbook. It allows users to find chapters, sections, or specific topics within the textbook structure.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for content navigation | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Python scripts for navigation operations | On Demand |
| `assets/` | Optional | Table of contents and content mapping data | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Input Validation**: Verify that the content query or location request is provided.
2.  **Content Index Search**: Search the internal content index to find matches for the requested content.
3.  **Location Mapping**: Map the requested content to specific chapters, sections, or file paths.
4.  **Result Formatting**: Format the location results in a user-friendly way with proper citations.
5.  **Output Delivery**: Return the location information with direct references to where content can be found.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/content_navigation.py`
* **Invocation Command**: `python scripts/content_navigation.py --query "chapter about humanoid control" --max_results 3`
* **Configuration**: The script reads the table of contents from `assets/toc.json` which contains the mapping of content to locations.

### D. Inputs and Outputs

* **Inputs:**
    * `query`: The content to search for (string)
    * `max_results`: Maximum number of results to return (integer, default: 5)
* **Outputs:**
    * `results`: List of matching content locations
    * `chapter`: The chapter where content is found
    * `section`: The specific section within the chapter
    * `file_path`: The file path where content is stored
    * `relevance_score`: Score indicating how well the content matches the query

---

## 4. 🛠️ Error Handling

* **No Matches Found**: If no content matches the query, return a message indicating that the content may not exist or suggest alternative search terms.
* **Index Unavailable**: If the content index is unavailable, return an error message and suggest trying again later.