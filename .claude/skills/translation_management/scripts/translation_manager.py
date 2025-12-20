#!/usr/bin/env python3
"""
Translation Manager Script

This script manages multilingual content for the Physical AI & Humanoid Robotics textbook,
handling translation workflows, locale management, and cultural adaptation.
"""

import argparse
import json
import os
import re
from typing import Dict, List, Any

def load_locale_config():
    """Load locale configuration from assets/locale_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'locale_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default locale configuration
        return {
            "supported_locales": {
                "en": {
                    "name": "English",
                    "direction": "ltr",
                    "cultural_considerations": [],
                    "date_format": "MM/DD/YYYY",
                    "number_format": "1,234.56"
                },
                "ur": {
                    "name": "Urdu",
                    "direction": "rtl",
                    "cultural_considerations": [
                        "Right-to-left reading direction",
                        "Use appropriate honorifics",
                        "Consider religious sensitivities"
                    ],
                    "date_format": "DD/MM/YYYY",
                    "number_format": "1,234.56"
                },
                "es": {
                    "name": "Spanish",
                    "direction": "ltr",
                    "cultural_considerations": [
                        "Use appropriate formal/informal language",
                        "Consider regional variations"
                    ],
                    "date_format": "DD/MM/YYYY",
                    "number_format": "1.234,56"
                },
                "fr": {
                    "name": "French",
                    "direction": "ltr",
                    "cultural_considerations": [
                        "Use formal language in educational context",
                        "Consider regional variations"
                    ],
                    "date_format": "DD/MM/YYYY",
                    "number_format": "1 234,56"
                }
            },
            "translation_workflows": {
                "automated": {
                    "steps": ["machine_translation", "grammar_check"],
                    "quality_threshold": 0.7
                },
                "human_reviewed": {
                    "steps": ["machine_translation", "human_review", "proofreading"],
                    "quality_threshold": 0.95
                },
                "hybrid": {
                    "steps": ["machine_translation", "human_post_edit", "quality_assurance"],
                    "quality_threshold": 0.9
                }
            },
            "cultural_adaptation_rules": {
                "technical_terms": {
                    "preserve_in_source": ["AI", "robotics", "algorithm", "neural network"],
                    "transliterate": ["specific_technical_terms_that_have_local_equivalents"]
                },
                "examples_adaptation": {
                    "cultural_context": {
                        "en_to_ur": {
                            "adapt_examples": True,
                            "preserve_core_concept": True
                        }
                    }
                }
            }
        }

def extract_translatable_content(content: str) -> List[Dict[str, Any]]:
    """Extract translatable content from text."""

    # Patterns to identify translatable content
    patterns = [
        # Markdown headers
        (r'^(#+\s+)(.+)$', 'header'),
        # Regular paragraphs
        (r'^([^#\s].*)$', 'paragraph'),
        # Bold and italic text
        (r'\*\*(.*?)\*\*', 'bold'),
        (r'\*(.*?)\*', 'italic'),
        # Links
        (r'\[([^\]]+)\]\(([^)]+)\)', 'link'),
        # Code blocks (usually not translated)
        (r'`([^`]+)`', 'code'),
    ]

    content_elements = []

    for i, line in enumerate(content.split('\n'), 1):
        # Skip empty lines and code blocks
        if not line.strip() or line.strip().startswith('```'):
            continue

        # Check for headers
        header_match = re.match(r'^(#+\s+)(.+)$', line)
        if header_match:
            content_elements.append({
                "type": "header",
                "content": header_match.group(2).strip(),
                "original": line,
                "line_number": i,
                "should_translate": True
            })
            continue

        # Check for regular paragraphs and other content
        line_processed = False
        for pattern, content_type in patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                content_elements.append({
                    "type": content_type,
                    "content": match.group(1) if len(match.groups()) >= 1 else match.group(0),
                    "original": match.group(0),
                    "line_number": i,
                    "should_translate": content_type not in ['code', 'link']  # Don't translate code, but do translate link text
                })
                line_processed = True

        # If no specific pattern matched, treat as paragraph
        if not line_processed and not line.strip().startswith('#'):
            content_elements.append({
                "type": "paragraph",
                "content": line.strip(),
                "original": line,
                "line_number": i,
                "should_translate": True
            })

    return content_elements

def translate_content(content_elements: List[Dict[str, Any]], source_locale: str, target_locale: str) -> List[Dict[str, Any]]:
    """Simulate translation of content elements."""

    # This is a simplified translation simulation
    # In a real implementation, this would connect to a translation API
    translated_elements = []

    for element in content_elements:
        translated_element = element.copy()

        if element.get("should_translate", False):
            # Simulate translation by adding a prefix/suffix
            original_content = element["content"]

            # For demonstration, we'll just add translation markers
            # In real implementation, this would call a translation service
            if target_locale == "ur":
                # Simulate Urdu translation (in English for demonstration)
                translated_content = f"[URDU-TRANSLATION] {original_content} [END]"
            elif target_locale == "es":
                # Simulate Spanish translation
                translated_content = f"[SPANISH-TRANSLATION] {original_content} [END]"
            elif target_locale == "fr":
                # Simulate French translation
                translated_content = f"[FRENCH-TRANSLATION] {original_content} [END]"
            else:
                # Default case
                translated_content = f"[TRANSLATED-TO-{target_locale.upper()}] {original_content} [END]"

            translated_element["translated_content"] = translated_content
            translated_element["translation_quality"] = 0.85  # Simulated quality score
        else:
            # Content that shouldn't be translated (like code)
            translated_element["translated_content"] = element["content"]
            translated_element["translation_quality"] = 1.0

        translated_elements.append(translated_element)

    return translated_elements

def apply_cultural_adaptation(translated_elements: List[Dict[str, Any]], source_locale: str, target_locale: str) -> List[Dict[str, Any]]:
    """Apply cultural adaptations to translated content."""

    adapted_elements = []
    config = load_locale_config()

    for element in translated_elements:
        adapted_element = element.copy()

        # Apply cultural adaptations based on locale pair
        if source_locale == "en" and target_locale == "ur":
            # Specific adaptations for English to Urdu
            content = adapted_element.get("translated_content", "")
            # Example: Adapt technical examples to be more culturally relevant
            adapted_content = content.replace("[URDU-TRANSLATION]", "[URDU-TRANSLATION (CULTURALLY ADAPTED)]")
            adapted_element["translated_content"] = adapted_content

        adapted_elements.append(adapted_element)

    return adapted_elements

def generate_translation_report(original_elements: List[Dict[str, Any]],
                              translated_elements: List[Dict[str, Any]],
                              source_locale: str,
                              target_locale: str) -> Dict[str, Any]:
    """Generate a report on the translation process."""

    total_elements = len(translated_elements)
    translated_elements_count = len([e for e in translated_elements if e.get("should_translate", False)])
    avg_quality = sum([e.get("translation_quality", 0) for e in translated_elements]) / total_elements if total_elements > 0 else 0

    return {
        "source_locale": source_locale,
        "target_locale": target_locale,
        "total_elements": total_elements,
        "translated_elements": translated_elements_count,
        "average_quality": round(avg_quality, 2),
        "quality_assessment": "Good" if avg_quality >= 0.8 else "Needs Review" if avg_quality >= 0.6 else "Poor",
        "cultural_adaptations_applied": source_locale != target_locale,
        "recommendations": [
            "Review translations with quality score below 0.7",
            "Verify cultural appropriateness of examples",
            "Check for proper handling of technical terminology"
        ]
    }

def main():
    parser = argparse.ArgumentParser(description='Translation Manager')
    parser.add_argument('--source', type=str, default='en', help='Source language code')
    parser.add_argument('--target', type=str, required=True, help='Target language code')
    parser.add_argument('--content-path', type=str, required=True, help='Path to content that needs translation')
    parser.add_argument('--workflow', type=str, default='automated',
                       choices=['automated', 'human_reviewed', 'hybrid'],
                       help='Translation workflow to use')

    args = parser.parse_args()

    # Validate locales
    config = load_locale_config()
    if args.source not in config["supported_locales"]:
        print(json.dumps({
            "error": f"Source locale '{args.source}' is not supported",
            "supported_locales": list(config["supported_locales"].keys())
        }))
        return

    if args.target not in config["supported_locales"]:
        print(json.dumps({
            "error": f"Target locale '{args.target}' is not supported",
            "supported_locales": list(config["supported_locales"].keys())
        }))
        return

    # Read content from file
    try:
        with open(args.content_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(json.dumps({
            "error": f"Content file not found: {args.content_path}"
        }))
        return
    except Exception as e:
        print(json.dumps({
            "error": f"Error reading content file: {str(e)}"
        }))
        return

    # Extract translatable content
    content_elements = extract_translatable_content(content)

    # Translate content
    translated_elements = translate_content(content_elements, args.source, args.target)

    # Apply cultural adaptations
    adapted_elements = apply_cultural_adaptation(translated_elements, args.source, args.target)

    # Generate translation report
    report = generate_translation_report(content_elements, adapted_elements, args.source, args.target)

    # Prepare output
    output = {
        "input": {
            "source_locale": args.source,
            "target_locale": args.target,
            "content_path": args.content_path,
            "workflow": args.workflow
        },
        "translation_process": {
            "original_elements_count": len(content_elements),
            "translated_elements": adapted_elements
        },
        "report": report
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()