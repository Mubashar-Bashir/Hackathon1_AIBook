#!/usr/bin/env python3
"""
Content Navigation Skill Script

This script helps navigate and find specific content within the
Physical AI & Humanoid Robotics textbook.
"""

import argparse
import json
import os
from typing import List, Dict, Optional

def load_toc():
    """Load table of contents from assets/toc.json"""
    toc_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'toc.json')
    if os.path.exists(toc_path):
        with open(toc_path, 'r') as f:
            return json.load(f)
    else:
        # Default table of contents
        return {
            "Physical AI & Humanoid Robotics Textbook": {
                "Chapter 1: Foundations of Physical AI": {
                    "path": "docs/physical-ai/chapter1.md",
                    "sections": [
                        "1.1 Introduction to Physical AI",
                        "1.2 Defining Physical AI and Its Scope",
                        "1.3 Physical AI vs. Traditional AI: Key Differences",
                        "1.4 Core Concepts in Physical AI",
                        "1.5 Importance and Applications of Physical AI"
                    ]
                },
                "Chapter 2: Humanoid Robotics Fundamentals": {
                    "path": "docs/humanoid-robotics/chapter1.md",
                    "sections": [
                        "2.1 Introduction to Humanoid Robotics",
                        "2.2 Design Principles",
                        "2.3 Actuation and Control Systems",
                        "2.4 Sensory Systems",
                        "2.5 Applications and Use Cases"
                    ]
                },
                "Chapter 3: Advanced Control Systems": {
                    "path": "docs/humanoid-robotics/chapter2.md",
                    "sections": [
                        "3.1 Dynamic Control Strategies",
                        "3.2 Balance and Stability",
                        "3.3 Motion Planning",
                        "3.4 Adaptive Control",
                        "3.5 Human-Robot Interaction"
                    ]
                }
            }
        }

def search_content_index(query: str, toc: Dict, max_results: int = 5) -> List[Dict]:
    """
    Search the table of contents for content matching the query.
    This is a simple keyword matching implementation.
    """
    results = []

    query_lower = query.lower()

    for chapter_title, chapter_data in toc.items():
        # Check if query matches chapter title
        if query_lower in chapter_title.lower():
            results.append({
                "title": chapter_title,
                "type": "chapter",
                "path": chapter_data["path"],
                "relevance_score": 0.9
            })

        # Check sections within chapter
        for section in chapter_data.get("sections", []):
            if query_lower in section.lower():
                results.append({
                    "title": f"{chapter_title} - {section}",
                    "type": "section",
                    "path": chapter_data["path"],
                    "relevance_score": 0.8
                })

    # Sort by relevance score (descending) and return top results
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:max_results]

def main():
    parser = argparse.ArgumentParser(description='Content Navigation Skill')
    parser.add_argument('--query', type=str, required=True, help='The content to search for')
    parser.add_argument('--max_results', type=int, default=5, help='Maximum number of results to return')

    args = parser.parse_args()

    # Load table of contents
    toc = load_toc()

    # Search for content
    results = search_content_index(args.query, toc, args.max_results)

    # Prepare output
    output = {
        "query": args.query,
        "results": results,
        "total_found": len(results)
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()