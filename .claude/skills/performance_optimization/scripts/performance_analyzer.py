#!/usr/bin/env python3
"""
Performance Analyzer Script

This script analyzes and optimizes application performance for the Physical AI & Humanoid Robotics textbook project.
"""

import argparse
import json
import os
import subprocess
import sys
from typing import Dict, List, Any

def load_optimization_techniques():
    """Load optimization techniques from assets/optimization_techniques.json"""
    techniques_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'optimization_techniques.json')
    if os.path.exists(techniques_path):
        with open(techniques_path, 'r') as f:
            return json.load(f)
    else:
        # Default optimization techniques
        return {
            "web_optimizations": {
                "bundle_size": {
                    "techniques": [
                        "Code splitting",
                        "Tree shaking",
                        "Minification",
                        "Compression (Gzip/Brotli)",
                        "Unused code removal",
                        "Dynamic imports"
                    ],
                    "tools": ["Webpack Bundle Analyzer", "Rollup", "Terser", "Babel-minify"],
                    "benchmarks": {
                        "good": 200000,  # 200KB
                        "acceptable": 500000,  # 500KB
                        "needs_improvement": 1000000  # 1MB
                    }
                },
                "loading_time": {
                    "techniques": [
                        "Lazy loading",
                        "Preloading",
                        "Caching strategies",
                        "CDN usage",
                        "Image optimization",
                        "Critical CSS inlining"
                    ],
                    "benchmarks": {
                        "good": 2.0,  # 2 seconds
                        "acceptable": 3.0,  # 3 seconds
                        "needs_improvement": 5.0  # 5 seconds
                    }
                },
                "rendering": {
                    "techniques": [
                        "Virtual scrolling",
                        "Debouncing/throttling",
                        "Efficient re-rendering",
                        "Web workers",
                        "Progressive loading"
                    ]
                }
            },
            "mobile_optimizations": {
                "battery_usage": {
                    "techniques": [
                        "Efficient background processing",
                        "Optimized network requests",
                        "Reduced animations",
                        "Efficient algorithms"
                    ]
                },
                "memory_usage": {
                    "techniques": [
                        "Memory leak prevention",
                        "Efficient data structures",
                        "Resource cleanup",
                        "Image caching"
                    ]
                }
            },
            "general_principles": [
                "Minimize HTTP requests",
                "Optimize images and assets",
                "Use efficient algorithms",
                "Implement proper caching",
                "Reduce render-blocking resources",
                "Optimize database queries",
                "Use content delivery networks"
            ]
        }

def analyze_project_structure(project_path: str) -> Dict[str, Any]:
    """Analyze the project structure for potential performance issues."""

    analysis = {
        "project_path": project_path,
        "file_counts": {},
        "size_analysis": {},
        "potential_issues": []
    }

    # Count different types of files
    file_extensions = {
        "js": 0, "ts": 0, "jsx": 0, "tsx": 0,  # JavaScript/TypeScript
        "css": 0, "scss": 0, "sass": 0,  # Styles
        "html": 0,  # HTML
        "json": 0,  # JSON
        "py": 0,  # Python
        "md": 0,  # Markdown
        "jpg": 0, "jpeg": 0, "png": 0, "gif": 0, "svg": 0,  # Images
        "pdf": 0, "doc": 0, "docx": 0  # Documents
    }

    total_size = 0

    for root, dirs, files in os.walk(project_path):
        # Skip node_modules and other large directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build']]

        for file in files:
            # Get file extension
            _, ext = os.path.splitext(file)
            ext = ext.lower().lstrip('.')

            if ext in file_extensions:
                file_extensions[ext] += 1

            # Calculate file size
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size
            except OSError:
                # Skip files that can't be accessed
                continue

    analysis["file_counts"] = {k: v for k, v in file_extensions.items() if v > 0}
    analysis["total_size"] = total_size
    analysis["total_size_mb"] = round(total_size / (1024 * 1024), 2)

    # Identify potential issues
    if file_extensions["js"] + file_extensions["ts"] + file_extensions["jsx"] + file_extensions["tsx"] > 100:
        analysis["potential_issues"].append({
            "type": "high_js_count",
            "severity": "medium",
            "description": "High number of JavaScript/TypeScript files - consider code splitting or bundling optimization",
            "recommendation": "Implement code splitting and lazy loading for better performance"
        })

    if file_extensions["jpg"] + file_extensions["jpeg"] + file_extensions["png"] > 20:
        analysis["potential_issues"].append({
            "type": "high_image_count",
            "severity": "medium",
            "description": "High number of image files - consider optimization or lazy loading",
            "recommendation": "Implement image optimization and lazy loading techniques"
        })

    if total_size > 100 * 1024 * 1024:  # 100MB
        analysis["potential_issues"].append({
            "type": "large_project_size",
            "severity": "high",
            "description": "Project size exceeds recommended limits",
            "recommendation": "Review and optimize large files, implement proper asset management"
        })

    return analysis

def generate_optimization_recommendations(project_analysis: Dict[str, Any], target: str) -> Dict[str, Any]:
    """Generate optimization recommendations based on project analysis."""

    techniques = load_optimization_techniques()
    recommendations = {
        "high_priority": [],
        "medium_priority": [],
        "low_priority": [],
        "expected_improvements": {}
    }

    # High priority recommendations based on critical issues
    for issue in project_analysis.get("potential_issues", []):
        if issue["severity"] == "high":
            recommendations["high_priority"].append({
                "issue": issue["description"],
                "recommendation": issue["recommendation"],
                "implementation_effort": "high",
                "expected_impact": "high"
            })

    # Additional recommendations based on target platform
    if target == "web":
        web_techs = techniques["web_optimizations"]

        # Bundle size recommendations
        if project_analysis.get("total_size", 0) > web_techs["bundle_size"]["benchmarks"]["needs_improvement"]:
            recommendations["high_priority"].append({
                "issue": "Bundle size exceeds recommended limits",
                "recommendation": "Implement code splitting, tree shaking, and minification",
                "implementation_effort": "medium",
                "expected_impact": "high",
                "techniques": web_techs["bundle_size"]["techniques"]
            })

        recommendations["medium_priority"].extend([
            {
                "issue": "Optimize loading performance",
                "recommendation": "Implement lazy loading and caching strategies",
                "implementation_effort": "medium",
                "expected_impact": "medium",
                "techniques": web_techs["loading_time"]["techniques"]
            },
            {
                "issue": "Optimize rendering performance",
                "recommendation": "Implement efficient re-rendering and virtual scrolling",
                "implementation_effort": "high",
                "expected_impact": "medium",
                "techniques": web_techs["rendering"]["techniques"]
            }
        ])

    # General recommendations
    recommendations["low_priority"].append({
        "issue": "General performance improvements",
        "recommendation": "Follow general performance optimization principles",
        "implementation_effort": "low",
        "expected_impact": "low",
        "techniques": techniques["general_principles"]
    })

    # Calculate expected improvements
    size_reduction_estimate = 0
    if project_analysis.get("total_size", 0) > web_techs["bundle_size"]["benchmarks"]["needs_improvement"]:
        size_reduction_estimate = 0.3  # 30% reduction estimate

    recommendations["expected_improvements"] = {
        "bundle_size_reduction": f"{size_reduction_estimate*100:.0f}% estimated",
        "loading_time_improvement": "20-40% estimated",
        "rendering_performance": "Improved with proper implementation"
    }

    return recommendations

def main():
    parser = argparse.ArgumentParser(description='Performance Analyzer')
    parser.add_argument('--project-path', type=str, required=True, help='Path to the project to analyze')
    parser.add_argument('--target', type=str, default='web',
                       choices=['web', 'mobile', 'desktop'],
                       help='Target platform')
    parser.add_argument('--metrics', type=str, default='bundle-size,loading-time',
                       help='Comma-separated list of performance metrics to evaluate')

    args = parser.parse_args()

    # Validate project path
    if not os.path.exists(args.project_path):
        print(json.dumps({
            "error": f"Project path does not exist: {args.project_path}",
            "available_options": ["web", "mobile", "desktop"]
        }))
        sys.exit(1)

    # Analyze project structure
    project_analysis = analyze_project_structure(args.project_path)

    # Generate optimization recommendations
    recommendations = generate_optimization_recommendations(project_analysis, args.target)

    # Prepare output
    output = {
        "input": {
            "project_path": args.project_path,
            "target": args.target,
            "metrics": args.metrics.split(',')
        },
        "analysis": project_analysis,
        "recommendations": recommendations
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()