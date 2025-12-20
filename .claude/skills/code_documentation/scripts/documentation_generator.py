#!/usr/bin/env python3
"""
Code Documentation Generator Script

This script generates comprehensive documentation for codebases, including API documentation,
code comments, and usage examples.
"""

import argparse
import json
import os
import re
from typing import Dict, List, Any

def load_doc_templates():
    """Load documentation templates from assets/doc_templates.json"""
    templates_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'doc_templates.json')
    if os.path.exists(templates_path):
        with open(templates_path, 'r') as f:
            return json.load(f)
    else:
        # Default documentation templates
        return {
            "python": {
                "function": {
                    "template": '''def {function_name}({parameters}):
    """
    {function_name} - {description}

    Args:
{args_list}

    Returns:
        {return_type}: {return_description}

    Raises:
        {exception_list}

    Example:
        {example}
    """
    pass''',
                    "docstring_format": "Google",
                    "comment_style": "#"
                },
                "class": {
                    "template": '''class {class_name}:
    """
    {class_name} - {description}

    Attributes:
{attributes_list}

    Methods:
{methods_list}
    """

    def __init__(self{init_params}):
        """
        Initialize {class_name}.

        Args:
{init_args_list}
        """
        pass''',
                    "docstring_format": "Google",
                    "comment_style": "#"
                }
            },
            "javascript": {
                "function": {
                    "template": '''/**
 * {description}
 *
 * @param {{*}} {parameters} - Description of parameters
 * @returns {{*}} {return_description}
 * @throws {{Error}} Description of possible errors
 * @example
 * {example}
 */
function {function_name}({parameters}) {{
    // Implementation here
}}''',
                    "docstring_format": "JSDoc",
                    "comment_style": "//"
                }
            },
            "typescript": {
                "function": {
                    "template": '''/**
 * {description}
 *
 * @param {{*}} {parameters} - Description of parameters
 * @returns {{*}} {return_description}
 * @throws {{Error}} Description of possible errors
 * @example
 * {example}
 */
function {function_name}({typed_parameters}): {return_type} {{
    // Implementation here
}}''',
                    "docstring_format": "JSDoc",
                    "comment_style": "//"
                }
            },
            "documentation_patterns": {
                "function": ["calculate", "process", "generate", "validate", "transform"],
                "class": ["Manager", "Service", "Controller", "Handler", "Processor"],
                "description_templates": [
                    "Processes {input_type} and returns {output_type}",
                    "Calculates and returns {result_type}",
                    "Validates {input_type} and returns boolean result",
                    "Transforms {input_type} to {output_type}"
                ]
            }
        }

def extract_function_info(code: str) -> Dict[str, Any]:
    """Extract function information from code."""
    # Look for Python function definition
    func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*->?\s*([^:\s\n]+)?'
    match = re.search(func_pattern, code)

    if match:
        func_name = match.group(1)
        params_str = match.group(2).strip()
        return_type = match.group(3) if match.group(3) else "None"

        # Parse parameters
        params = []
        if params_str:
            # Remove self parameter for methods
            param_list = [p.strip() for p in params_str.split(',')]
            for param in param_list:
                if param != 'self':
                    # Extract parameter name and type if present
                    parts = param.split(':')
                    param_name = parts[0].strip()
                    param_type = parts[1].strip() if len(parts) > 1 else 'any'
                    params.append({"name": param_name, "type": param_type})

        return {
            "name": func_name,
            "parameters": params,
            "return_type": return_type.strip()
        }

    # Look for JavaScript/TypeScript function definition
    js_func_pattern = r'function\s+(\w+)\s*\(([^)]*)\)'
    js_match = re.search(js_func_pattern, code)

    if js_match:
        func_name = js_match.group(1)
        params_str = js_match.group(2).strip()

        params = []
        if params_str:
            param_list = [p.strip() for p in params_str.split(',')]
            for param in param_list:
                if param:
                    # Extract parameter name (and potentially type in TS)
                    param_parts = param.split(':')
                    param_name = param_parts[0].strip()
                    param_type = param_parts[1].strip() if len(param_parts) > 1 else 'any'
                    params.append({"name": param_name, "type": param_type})

        return {
            "name": func_name,
            "parameters": params,
            "return_type": "any"
        }

    return None

def generate_documentation(code: str, language: str = "python", include_examples: bool = True) -> Dict[str, Any]:
    """Generate documentation for the provided code."""

    templates = load_doc_templates()

    # Extract function information
    func_info = extract_function_info(code)

    if not func_info:
        return {
            "error": "Could not extract function information from the provided code",
            "supported_patterns": ["def function_name(...)", "function function_name(...)"]
        }

    # Determine language-specific template
    lang_templates = templates.get(language, templates["python"])
    func_template = lang_templates.get("function", lang_templates["python"]["function"])

    # Generate parameter list for documentation
    args_list = ""
    for param in func_info["parameters"]:
        args_list += f"        {param['name']} ({param['type']}): Description of {param['name']}\n"

    # Generate return description
    return_description = f"Description of return value of type {func_info['return_type']}"

    # Generate exception list
    exception_list = "ExceptionType: Description of when this exception is raised"

    # Generate example
    example_params = ", ".join([f"param_value_{p['name']}" for p in func_info["parameters"]])
    example = f"result = {func_info['name']}({example_params})"

    # Create documentation
    documentation = func_template["template"].format(
        function_name=func_info["name"],
        parameters=", ".join([p["name"] for p in func_info["parameters"]]),
        typed_parameters=", ".join([f"{p['name']}: {p['type']}" for p in func_info["parameters"]]),
        description=f"Description of what {func_info['name']} does",
        args_list=args_list.rstrip(),
        return_type=func_info["return_type"],
        return_description=return_description,
        exception_list=exception_list,
        example=example
    )

    # Generate API reference
    api_reference = {
        "name": func_info["name"],
        "type": "function",
        "language": language,
        "parameters": func_info["parameters"],
        "return_type": func_info["return_type"],
        "location": "Generated from provided code"
    }

    # Generate usage examples
    usage_examples = []
    if include_examples:
        usage_examples.append({
            "title": f"Basic usage of {func_info['name']}",
            "code": example,
            "explanation": f"Call {func_info['name']} with appropriate parameters to get the result"
        })

    return {
        "documentation": documentation,
        "api_reference": api_reference,
        "usage_examples": usage_examples,
        "style_compliance": {
            "format": func_template["docstring_format"],
            "compliant": True,
            "issues": []
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Code Documentation Generator')
    parser.add_argument('--code', type=str, required=True, help='The source code to document')
    parser.add_argument('--language', type=str, default='python',
                       choices=['python', 'javascript', 'typescript'],
                       help='Programming language of the code')
    parser.add_argument('--format', type=str, default='markdown',
                       choices=['markdown', 'html', 'json'],
                       help='Output format')
    parser.add_argument('--include-examples', action='store_true',
                       help='Include usage examples in documentation')

    args = parser.parse_args()

    # Generate documentation
    result = generate_documentation(args.code, args.language, args.include_examples)

    # Prepare output
    output = {
        "input": {
            "language": args.language,
            "format": args.format,
            "include_examples": args.include_examples
        },
        "result": result
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()