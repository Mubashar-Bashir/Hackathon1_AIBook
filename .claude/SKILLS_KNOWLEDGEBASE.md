# Project Skills Knowledgebase

## Overview
This document serves as a comprehensive reference for all available skills in the Physical AI & Humanoid Robotics Textbook project. These skills follow the AIDD (Agent IDD) framework and provide specialized capabilities for various development tasks.

## Available Skills

### 1. Content Structure Skill
- **Name**: ContentStructureSkill
- **Purpose**: Helps organize textbook content into proper learning modules with appropriate structure, learning objectives, and pedagogical flow
- **Key Features**:
  - Content analysis and structure planning
  - Learning objective setting
  - Educational framework alignment
  - Assessment integration
- **Usage**: `python .claude/skills/content_structure/scripts/content_structure_analyzer.py --topic "Physical AI foundations" --level "undergraduate" --sections 5`

### 2. Educational Assessment Skill
- **Name**: EducationalAssessmentSkill
- **Purpose**: Creates quizzes, exercises, and assessments for learning modules with appropriate difficulty levels
- **Key Features**:
  - Multiple question type generation (multiple choice, short answer, true/false, etc.)
  - Difficulty level customization
  - Grading rubric development
  - Pedagogical alignment
- **Usage**: `python .claude/skills/educational_assessment/scripts/assessment_generator.py --topic "Physical AI concepts" --level "undergraduate" --question-count 10 --types "multiple-choice,short-answer"`

### 3. Code Documentation Skill
- **Name**: CodeDocumentationSkill
- **Purpose**: Generates comprehensive documentation for codebases including API docs and usage examples
- **Key Features**:
  - Multi-language support (Python, JavaScript, TypeScript)
  - API reference generation
  - Usage example creation
  - Style consistency enforcement
- **Usage**: `python .claude/skills/code_documentation/scripts/documentation_generator.py --code "function_code" --language "python" --format "markdown"`

### 4. Performance Optimization Skill
- **Name**: PerformanceOptimizationSkill
- **Purpose**: Analyzes and optimizes application performance focusing on bundle size, loading times, and resource efficiency
- **Key Features**:
  - Bundle size analysis
  - Loading time optimization
  - Performance bottleneck identification
  - Optimization recommendations
- **Usage**: `python .claude/skills/performance_optimization/scripts/performance_analyzer.py --project-path "./book" --target "web" --metrics "bundle-size,loading-time"`

### 5. Security Audit Skill
- **Name**: SecurityAuditSkill
- **Purpose**: Performs security analysis identifying vulnerabilities and ensuring security best practices
- **Key Features**:
  - SAST (Static Application Security Testing)
  - Dependency vulnerability scanning
  - Configuration review
  - Compliance checking
- **Usage**: `python .claude/skills/security_audit/scripts/security_scanner.py --project-path "./backend" --check-types "sast,dependencies,config"`

### 6. Translation Management Skill
- **Name**: TranslationManagementSkill
- **Purpose**: Manages multilingual content handling translation workflows and cultural adaptation
- **Key Features**:
  - Multi-language support (English, Urdu, Spanish, French, etc.)
  - Cultural adaptation
  - Translation quality assessment
  - Workflow management
- **Usage**: `python .claude/skills/translation_management/scripts/translation_manager.py --source "en" --target "ur" --content-path "./book/docs" --workflow "automated-review"`

### 7. Testing Strategy Skill
- **Name**: TestingStrategySkill
- **Purpose**: Creates comprehensive testing plans covering unit, integration, and end-to-end tests
- **Key Features**:
  - Test plan generation
  - Coverage target setting
  - Framework recommendations
  - Quality metrics definition
- **Usage**: `python .claude/skills/testing_strategy/scripts/test_strategy_generator.py --project-path "./backend" --coverage-target 80 --test-types "unit,integration,e2e"`

### 8. Deployment Configuration Skill
- **Name**: DeploymentConfigurationSkill
- **Purpose**: Sets up deployment configurations for different environments with CI/CD pipelines
- **Key Features**:
  - Multi-platform support (Docker, Kubernetes, Vercel, AWS)
  - Environment-specific configurations
  - CI/CD pipeline setup
  - Scaling strategy definition
- **Usage**: `python .claude/skills/deployment_configuration/scripts/deployment_configurator.py --project-path "./backend" --target-environment "production" --deployment-platform "docker"`

### 9. UI/UX Components Skill
- **Name**: UIUXComponentsSkill
- **Purpose**: Creates and manages reusable UI components following design system principles
- **Key Features**:
  - Component generation for React/TypeScript
  - Design token application
  - Accessibility integration
  - Responsive design patterns
- **Usage**: `python .claude/skills/ui_ux_components/scripts/component_generator.py --type "button" --props "variant, size, disabled" --design-system "material"`

### 10. Accessibility Checker Skill
- **Name**: AccessibilityCheckerSkill
- **Purpose**: Checks UI components for accessibility compliance according to WCAG 2.1 standards
- **Key Features**:
  - WCAG 2.1 AA compliance checking
  - Issue identification and severity ranking
  - Remediation recommendations
  - Compliance scoring
- **Usage**: `python .claude/skills/accessibility_checker/scripts/accessibility_checker.py --input "component_code" --level "AA"`

### 11. Design System Skill
- **Name**: DesignSystemSkill
- **Purpose**: Maintains consistent design patterns and component libraries
- **Key Features**:
  - Design token management
  - Component consistency
  - Style guide enforcement
  - Pattern library maintenance

### 12. Responsive Layout Skill
- **Name**: ResponsiveLayoutSkill
- **Purpose**: Creates responsive layouts that work across different devices and screen sizes
- **Key Features**:
  - Breakpoint management
  - Grid system generation
  - Mobile-first approach
  - Cross-device compatibility

## Available Agents

### UI/UX Expert Agent
- **Name**: UIUXExpertAgent
- **Capabilities**: Interface design, accessibility compliance, responsive layouts, user research, prototyping
- **Authorized Skills**: UIUXComponentsSkill, AccessibilityCheckerSkill, DesignSystemSkill, ResponsiveLayoutSkill
- **Usage**: Can be invoked through the skills API to handle UI/UX related tasks

## How to Use These Skills in Development

### Direct Script Usage
1. Navigate to the skill's scripts directory
2. Run the appropriate script with required parameters
3. Use the generated output in your development process

### API Integration
All skills are integrated into the backend API at `/skills/` endpoints:
- `POST /skills/execute` - Execute any skill by name
- `GET /skills/list` - List all available skills
- Specific endpoints for each skill type

### Agent Integration
The UI/UX Expert Agent can be invoked through the agents API at `/agents/` endpoints:
- `POST /agents/execute` - Execute any agent with a query
- `GET /agents/list` - List all available agents

## Best Practices for Skill Usage

1. **Plan Before Implementation**: Use the Content Structure Skill to plan modules before coding
2. **Security First**: Run Security Audit Skill regularly during development
3. **Performance Conscious**: Use Performance Optimization Skill early and often
4. **Documentation Driven**: Generate documentation as you develop using Code Documentation Skill
5. **Test Early**: Create tests using Testing Strategy Skill from the beginning
6. **Accessible by Design**: Run Accessibility Checker Skill on all UI components
7. **International Ready**: Plan for translation using Translation Management Skill
8. **Deploy Ready**: Set up deployment configurations early with Deployment Configuration Skill

## Integration Points

These skills are integrated with:
- The main backend at `/skills/` and `/agents/` API endpoints
- The existing RAG system for enhanced functionality
- The authentication and personalization systems
- The content management pipeline

## Maintenance Guidelines

- Skills are located in `.claude/skills/` directory
- Agents are located in `.claude/agents/` directory
- Each skill follows the standard structure with metadata, instructions, scripts, and assets
- Skills can be extended by adding new scripts or modifying existing ones
- New skills should follow the same AIDD framework pattern

## Future Expansion

This skills framework is designed to be extensible. New skills can be added by:
1. Creating a new directory in `.claude/skills/`
2. Adding the required metadata and instruction files
3. Implementing the functionality in scripts
4. Registering with the API in `backend/src/api/skills_agents.py`

These skills provide a comprehensive toolkit for developing the Physical AI & Humanoid Robotics Textbook project with high quality, security, performance, and accessibility standards.