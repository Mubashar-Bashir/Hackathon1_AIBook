# UI/UX Components Skill

## 1. 🎯 Purpose and Philosophy

This skill enables the creation and management of reusable UI components for the Physical AI & Humanoid Robotics textbook interface. It ensures consistent, accessible, and well-designed components that enhance the learning experience.

---

## 2. 📂 Skill Structure and File System

| File/Folder Name | Required | Purpose | Disclosure Level |
| :--- | :--- | :--- | :--- |
| `skill_instructions.md` | **Mandatory** | Contains the core instructions for UI/UX component creation | Progressive |
| `skill_metadata.json` | **Mandatory** | Metadata for skill discovery | Progressive (Initial) |
| `scripts/` | Optional | Scripts for component generation and management | On Demand |
| `assets/` | Optional | Component templates, design tokens, and configurations | On Demand |

---

## 3. 🧠 Procedural Steps (The "How")

1.  **Component Analysis**: Analyze the requested component type and requirements.
2.  **Design Token Application**: Apply appropriate design tokens (colors, typography, spacing) from the design system.
3.  **Accessibility Integration**: Ensure the component meets accessibility standards (WCAG 2.1 AA).
4.  **Component Generation**: Generate the component code with proper TypeScript/JavaScript, CSS, and documentation.
5.  **Testing Preparation**: Include basic testing hooks and considerations.
6.  **Documentation Creation**: Generate usage documentation and examples.

### C. Tool/Script Usage (The "Whom/Invocation")

* **Script Location**: `scripts/component_generator.py`
* **Invocation Command**: `python scripts/component_generator.py --type "button" --props "variant, size, disabled" --design-system "material"`
* **Configuration**: The script reads design tokens from `assets/design_tokens.json` which contains color palettes, typography scales, and spacing units.

### D. Inputs and Outputs

* **Inputs:**
    * `component_type`: The type of component to create (e.g., button, card, modal, input)
    * `props`: Component properties and their types
    * `design_system`: The design system to follow (e.g., material, bootstrap, custom)
    * `accessibility_level`: Required accessibility compliance level
* **Outputs:**
    * `component_code`: The generated component code
    * `css_styles`: Associated styles for the component
    * `documentation`: Usage examples and guidelines
    * `test_hooks`: Testing considerations and hooks

---

## 4. 🛠️ Error Handling

* **Invalid Component Type**: If the requested component type is not supported, return available component types.
* **Accessibility Violations**: If the generated component doesn't meet accessibility requirements, flag the issues and suggest fixes.
* **Design System Conflicts**: If requested styles conflict with the design system, suggest alternatives or flag the conflict.