#!/usr/bin/env python3
"""
Test Strategy Generator Script

This script creates comprehensive testing plans and strategies for the Physical AI & Humanoid Robotics textbook project.
"""

import argparse
import json
import os
import re
from typing import Dict, List, Any

def load_testing_standards():
    """Load testing standards from assets/testing_standards.json"""
    standards_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'testing_standards.json')
    if os.path.exists(standards_path):
        with open(standards_path, 'r') as f:
            return json.load(f)
    else:
        # Default testing standards
        return {
            "test_types": {
                "unit": {
                    "description": "Test individual functions/components in isolation",
                    "coverage_target": 90,
                    "best_practices": [
                        "Test one thing at a time",
                        "Use mocks for external dependencies",
                        "Follow AAA pattern (Arrange, Act, Assert)"
                    ]
                },
                "integration": {
                    "description": "Test interactions between components/modules",
                    "coverage_target": 80,
                    "best_practices": [
                        "Test real component interactions",
                        "Use test databases where applicable",
                        "Test API endpoints with real data"
                    ]
                },
                "e2e": {
                    "description": "Test complete user workflows",
                    "coverage_target": 70,
                    "best_practices": [
                        "Test critical user journeys",
                        "Use realistic test data",
                        "Run in environments similar to production"
                    ]
                }
            },
            "quality_metrics": {
                "coverage": {
                    "minimum": 80,
                    "recommended": 90,
                    "excellent": 95
                },
                "mutation_score": {
                    "minimum": 60,
                    "recommended": 80,
                    "excellent": 90
                },
                "performance": {
                    "response_time": "< 200ms",
                    "throughput": "> 1000 requests/second"
                }
            },
            "testing_frameworks": {
                "python": {
                    "unit": ["pytest", "unittest"],
                    "integration": ["pytest", "requests"],
                    "e2e": ["Selenium", "Playwright", "pytest-playwright"]
                },
                "javascript": {
                    "unit": ["Jest", "Mocha", "Jasmine"],
                    "integration": ["Jest", "Supertest"],
                    "e2e": ["Cypress", "Playwright", "Puppeteer"]
                }
            }
        }

def analyze_project_structure(project_path: str) -> Dict[str, Any]:
    """Analyze the project structure to identify testable components."""

    analysis = {
        "project_path": project_path,
        "components": {
            "python": [],
            "javascript": [],
            "frontend": [],
            "backend": [],
            "api_endpoints": [],
            "models": [],
            "services": [],
            "utils": []
        },
        "testable_modules": []
    }

    # Walk through the project and identify different types of files
    for root, dirs, files in os.walk(project_path):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv', '.venv', '.next', 'dist', 'build', 'tests', 'test']]

        for file in files:
            file_path = os.path.join(root, file)

            # Identify Python files
            if file.endswith('.py'):
                # Skip test files
                if 'test' not in file.lower() and 'spec' not in file.lower():
                    analysis["components"]["python"].append(file_path)

                    # Identify different types of Python modules
                    if 'model' in file or 'entity' in file:
                        analysis["components"]["models"].append(file_path)
                    elif 'service' in file or 'manager' in file:
                        analysis["components"]["services"].append(file_path)
                    elif 'util' in file or 'helper' in file:
                        analysis["components"]["utils"].append(file_path)
                    elif 'api' in file or 'route' in file or 'endpoint' in file:
                        analysis["components"]["api_endpoints"].append(file_path)

            # Identify JavaScript/TypeScript files
            elif file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                if 'test' not in file.lower() and 'spec' not in file.lower():
                    analysis["components"]["javascript"].append(file_path)

                    # Identify frontend vs backend JS
                    if any(frontend_dir in root for frontend_dir in ['frontend', 'client', 'src/client', 'book']):
                        analysis["components"]["frontend"].append(file_path)
                    else:
                        analysis["components"]["backend"].append(file_path)

    # Create a list of testable modules with their types
    for module_type, modules in analysis["components"].items():
        if module_type not in ['python', 'javascript', 'frontend', 'backend']:  # Skip the high-level categories
            for module in modules:
                analysis["testable_modules"].append({
                    "path": module,
                    "type": module_type,
                    "language": "python" if module.endswith('.py') else "javascript",
                    "name": os.path.basename(module)
                })

    return analysis

def generate_test_plan(project_analysis: Dict[str, Any], coverage_target: int, test_types: List[str]) -> Dict[str, Any]:
    """Generate a comprehensive test plan based on project analysis."""

    standards = load_testing_standards()

    test_plan = {
        "project_path": project_analysis["project_path"],
        "coverage_target": coverage_target,
        "test_types": test_types,
        "components": [],
        "test_cases": [],
        "recommended_testing_approach": {}
    }

    # Generate test recommendations for each component
    for module in project_analysis["testable_modules"]:
        component_tests = {
            "component": module["path"],
            "type": module["type"],
            "language": module["language"],
            "recommended_tests": []
        }

        # Determine what types of tests to recommend based on component type
        if module["type"] in ["models", "utils"]:
            # Unit tests for models and utilities
            if "unit" in test_types:
                component_tests["recommended_tests"].append({
                    "type": "unit",
                    "description": f"Unit tests for {module['name']}",
                    "coverage_target": standards["test_types"]["unit"]["coverage_target"],
                    "framework": standards["testing_frameworks"][module["language"]]["unit"][0],
                    "best_practices": standards["test_types"]["unit"]["best_practices"]
                })

        elif module["type"] in ["services"]:
            # Unit and integration tests for services
            if "unit" in test_types:
                component_tests["recommended_tests"].append({
                    "type": "unit",
                    "description": f"Unit tests for {module['name']} business logic",
                    "coverage_target": standards["test_types"]["unit"]["coverage_target"],
                    "framework": standards["testing_frameworks"][module["language"]]["unit"][0],
                    "best_practices": standards["test_types"]["unit"]["best_practices"]
                })

            if "integration" in test_types:
                component_tests["recommended_tests"].append({
                    "type": "integration",
                    "description": f"Integration tests for {module['name']} with dependencies",
                    "coverage_target": standards["test_types"]["integration"]["coverage_target"],
                    "framework": standards["testing_frameworks"][module["language"]]["integration"][0],
                    "best_practices": standards["test_types"]["integration"]["best_practices"]
                })

        elif module["type"] in ["api_endpoints"]:
            # Integration and e2e tests for API endpoints
            if "integration" in test_types:
                component_tests["recommended_tests"].append({
                    "type": "integration",
                    "description": f"Integration tests for {module['name']} endpoints",
                    "coverage_target": standards["test_types"]["integration"]["coverage_target"],
                    "framework": standards["testing_frameworks"][module["language"]]["integration"][0],
                    "best_practices": standards["test_types"]["integration"]["best_practices"]
                })

            if "e2e" in test_types:
                component_tests["recommended_tests"].append({
                    "type": "e2e",
                    "description": f"End-to-end tests for {module['name']} workflows",
                    "coverage_target": standards["test_types"]["e2e"]["coverage_target"],
                    "framework": standards["testing_frameworks"][module["language"]]["e2e"][0],
                    "best_practices": standards["test_types"]["e2e"]["best_practices"]
                })

        test_plan["components"].append(component_tests)

    # Generate high-level test strategy
    test_plan["recommended_testing_approach"] = {
        "coverage_strategy": {
            "target": f"{coverage_target}%",
            "measurement_tool": "coverage.py for Python, Istanbul for JavaScript",
            "reporting_frequency": "per commit"
        },
        "automation_strategy": {
            "ci_integration": "GitHub Actions, GitLab CI, or Jenkins",
            "trigger_events": ["push", "pull_request"],
            "environments": ["development", "staging"]
        },
        "quality_gates": {
            "minimum_coverage": standards["quality_metrics"]["coverage"]["minimum"],
            "maximum_flakiness": "5%",
            "performance_thresholds": standards["quality_metrics"]["performance"]
        }
    }

    return test_plan

def main():
    parser = argparse.ArgumentParser(description='Test Strategy Generator')
    parser.add_argument('--project-path', type=str, required=True, help='Path to the project to analyze')
    parser.add_argument('--coverage-target', type=int, default=80, help='Desired test coverage percentage')
    parser.add_argument('--test-types', type=str, default='unit,integration,e2e',
                       help='Comma-separated list of test types to generate')

    args = parser.parse_args()

    # Validate project path
    if not os.path.exists(args.project_path):
        print(json.dumps({
            "error": f"Project path does not exist: {args.project_path}"
        }))
        return

    # Parse test types
    test_types = [t.strip() for t in args.test_types.split(',')]

    # Analyze project structure
    project_analysis = analyze_project_structure(args.project_path)

    # Generate test plan
    test_plan = generate_test_plan(project_analysis, args.coverage_target, test_types)

    # Prepare output
    output = {
        "input": {
            "project_path": args.project_path,
            "coverage_target": args.coverage_target,
            "test_types": test_types
        },
        "test_plan": test_plan
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()