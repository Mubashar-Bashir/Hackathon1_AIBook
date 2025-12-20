# Performance Optimization Skill

## 1. 🎯 Purpose and Philosophy

This skill analyzes and optimizes application performance for the Physical AI & Humanoid Robotics textbook project, focusing on bundle size, loading times, and resource efficiency to ensure a smooth user experience.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for performance optimization | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for performance analysis and optimization | On Demand |
| `assets/` | Optional | Performance benchmarks, optimization techniques, and best practices | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Performance Analysis**: Analyze the current application for performance bottlenecks.
2.  **Resource Audit**: Evaluate bundle size, asset optimization, and resource loading.
3.  **Bottleneck Identification**: Identify specific areas for improvement.
4.  **Optimization Strategy**: Generate targeted optimization recommendations.
5.  **Implementation Guidance**: Provide specific steps for implementing optimizations.
6.  **Monitoring Setup**: Suggest performance monitoring approaches.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/performance_analyzer.py`
* **Invocation Command**: `python scripts/performance_analyzer.py --project-path "./book" --target "web" --metrics "bundle-size,loading-time"`
* **Configuration**: The script reads optimization techniques from `assets/optimization_techniques.json` which contains best practices and benchmarks.

### D. Inputs and Outputs

* **Inputs:**
    * `project_path`: Path to the project to analyze
    * `target`: Target platform (web, mobile, desktop)
    * `metrics`: Comma-separated list of performance metrics to evaluate
    * `baseline`: Baseline performance metrics for comparison
* **Outputs:**
    * `bottlenecks`: Identified performance bottlenecks
    * `optimization_recommendations`: Specific recommendations for improvements
    * `priority_ranking`: Prioritized list of optimizations
    * `expected_improvement`: Estimated performance gains

---

## 4. 🛠️ Error Handling

* **Inaccessible Project**: If the project path is invalid or inaccessible, return an error message.
* **Unsupported Target**: If the target platform is not supported, return available options.
* **Analysis Failure**: If analysis cannot be completed, provide specific error details.