# Deployment Configuration Skill

## 1. 🎯 Purpose and Philosophy

This skill sets up deployment configurations for different environments for the Physical AI & Humanoid Robotics textbook project, managing CI/CD pipelines, environment variables, and scaling strategies to ensure reliable and efficient deployments.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for deployment configuration | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for deployment setup and configuration | On Demand |
| `assets/` | Optional | Deployment templates, environment configurations, and infrastructure definitions | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Environment Analysis**: Analyze the project to determine deployment requirements.
2.  **Infrastructure Planning**: Plan the infrastructure needed for different environments.
3.  **Configuration Generation**: Generate configuration files for deployment.
4.  **CI/CD Pipeline Setup**: Create continuous integration and deployment pipelines.
5.  **Environment Management**: Set up environment-specific configurations and variables.
6.  **Scaling Strategy**: Define scaling strategies for different load scenarios.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/deployment_configurator.py`
* **Invocation Command**: `python scripts/deployment_configurator.py --project-path "./backend" --target-environment "production" --deployment-platform "docker"`
* **Configuration**: The script reads deployment patterns from `assets/deployment_patterns.json` which contains best practices and platform-specific configurations.

### D. Inputs and Outputs

* **Inputs:**
    * `project_path`: Path to the project to configure for deployment
    * `target_environment`: Target environment (development, staging, production)
    * `deployment_platform`: Platform for deployment (docker, kubernetes, vercel, etc.)
    * `scaling_requirements`: Scaling requirements (low, medium, high, auto)
* **Outputs:**
    * `configuration_files`: Generated configuration files for deployment
    * `environment_variables`: Required environment variables
    * `ci_cd_pipeline`: CI/CD pipeline configuration
    * `scaling_strategy`: Defined scaling strategy for the environment

---

## 4. 🛠️ Error Handling

* **Unsupported Platform**: If the deployment platform is not supported, return available options.
* **Missing Dependencies**: If required dependencies are missing, list what needs to be installed.
* **Configuration Conflicts**: If configuration conflicts are detected, provide resolution options.