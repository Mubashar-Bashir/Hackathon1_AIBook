#!/usr/bin/env python3
"""
Educational Assessment Generator Script

This script creates quizzes, exercises, and assessments for learning modules in the Physical AI & Humanoid Robotics textbook.
"""

import argparse
import json
import os
import random
from typing import Dict, List, Any

def load_question_templates():
    """Load question templates from assets/question_templates.json"""
    templates_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'question_templates.json')
    if os.path.exists(templates_path):
        with open(templates_path, 'r') as f:
            return json.load(f)
    else:
        # Default question templates
        return {
            "multiple_choice": [
                "What is the primary characteristic of {topic}?",
                "Which of the following best describes {topic}?",
                "In the context of {topic}, which statement is true?",
                "What is the main purpose of {topic}?",
                "Which component is essential for {topic}?"
            ],
            "short_answer": [
                "Explain the concept of {topic} in your own words.",
                "Describe the key features of {topic}.",
                "What are the main challenges in {topic}?",
                "How does {topic} differ from traditional approaches?",
                "List the primary applications of {topic}."
            ],
            "true_false": [
                "{topic} requires specialized hardware. (True/False)",
                "The primary goal of {topic} is to improve computational efficiency. (True/False)",
                "{topic} is only applicable to robotics applications. (True/False)",
                "Learning in {topic} systems requires labeled training data. (True/False)"
            ],
            "fill_in_blank": [
                "The process of {topic} involves _______.",
                "_______ is the primary challenge in implementing {topic}.",
                "In {topic}, the term _______ refers to _______.",
                "The main advantage of {topic} is _______."
            ],
            "difficulty_levels": {
                "high_school": {
                    "recall": 0.6,
                    "comprehension": 0.3,
                    "application": 0.1
                },
                "undergraduate": {
                    "recall": 0.3,
                    "comprehension": 0.4,
                    "application": 0.3
                },
                "graduate": {
                    "recall": 0.1,
                    "comprehension": 0.2,
                    "application": 0.4,
                    "analysis": 0.3
                }
            }
        }

def generate_assessment(topic: str, education_level: str, question_count: int, question_types: List[str]) -> Dict[str, Any]:
    """Generate educational assessment based on topic, level, and requirements."""

    templates = load_question_templates()

    # Determine difficulty distribution based on education level
    difficulty_dist = templates["difficulty_levels"].get(education_level, templates["difficulty_levels"]["undergraduate"])

    # Generate questions
    questions = []

    for i in range(question_count):
        # Select a random question type from the requested types
        q_type = random.choice(question_types)

        # Get a template for this question type
        if q_type in templates and len(templates[q_type]) > 0:
            template = random.choice(templates[q_type])
            question_text = template.format(topic=topic)

            # Generate appropriate answer choices and correct answer
            if q_type == "multiple_choice":
                # Generate 4 answer choices with one correct
                correct_answer = f"Correct answer for: {question_text}"
                wrong_answers = [
                    f"Distractor 1 for: {question_text}",
                    f"Distractor 2 for: {question_text}",
                    f"Distractor 3 for: {question_text}"
                ]

                # Shuffle the options
                all_answers = [correct_answer] + wrong_answers
                random.shuffle(all_answers)

                # Find the index of the correct answer after shuffling
                correct_index = all_answers.index(correct_answer)

                question = {
                    "id": f"q{i+1}",
                    "type": q_type,
                    "question": question_text,
                    "options": all_answers,
                    "correct_answer": correct_answer,
                    "correct_index": correct_index,
                    "explanation": f"Explanation for why '{correct_answer}' is correct",
                    "difficulty": random.choice(list(difficulty_dist.keys()))
                }
            elif q_type == "true_false":
                # For true/false, determine if the statement should be true or false
                is_true = random.choice([True, False])
                answer_text = "True" if is_true else "False"

                question = {
                    "id": f"q{i+1}",
                    "type": q_type,
                    "question": question_text,
                    "correct_answer": answer_text,
                    "explanation": f"Explanation for why this statement is {'true' if is_true else 'false'}",
                    "difficulty": random.choice(list(difficulty_dist.keys()))
                }
            elif q_type == "fill_in_blank":
                # Generate a sample answer for the blank
                sample_answer = f"Sample answer for: {question_text}"

                question = {
                    "id": f"q{i+1}",
                    "type": q_type,
                    "question": question_text,
                    "sample_answer": sample_answer,
                    "explanation": f"Guidelines for acceptable answers to: {question_text}",
                    "difficulty": random.choice(list(difficulty_dist.keys()))
                }
            else:  # short_answer and other open-ended types
                question = {
                    "id": f"q{i+1}",
                    "type": q_type,
                    "question": question_text,
                    "sample_answer": f"Sample answer for: {question_text}",
                    "grading_guidelines": f"Grading criteria for: {question_text}",
                    "difficulty": random.choice(list(difficulty_dist.keys()))
                }

            questions.append(question)
        else:
            # If no template exists for the requested type, create a generic question
            question = {
                "id": f"q{i+1}",
                "type": q_type,
                "question": f"Question about {topic} (type: {q_type})",
                "sample_answer": f"Sample answer for {topic}",
                "grading_guidelines": f"Grading criteria for {topic}",
                "difficulty": random.choice(list(difficulty_dist.keys()))
            }
            questions.append(question)

    return {
        "topic": topic,
        "education_level": education_level,
        "total_questions": question_count,
        "question_types": question_types,
        "questions": questions,
        "grading_rubric": {
            "multiple_choice": {"points": 1, "feedback": "Provide immediate feedback for each answer"},
            "short_answer": {"points": 5, "feedback": "Evaluate completeness, accuracy, and clarity"},
            "true_false": {"points": 1, "feedback": "Provide explanation for correct/incorrect answers"},
            "fill_in_blank": {"points": 2, "feedback": "Accept equivalent answers with proper justification"}
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Educational Assessment Generator')
    parser.add_argument('--topic', type=str, required=True, help='The subject matter to assess')
    parser.add_argument('--level', type=str, default='undergraduate',
                       choices=['high_school', 'undergraduate', 'graduate'],
                       help='Target education level')
    parser.add_argument('--question-count', type=int, default=5, help='Number of questions to generate')
    parser.add_argument('--types', type=str, default='multiple-choice',
                       help='Comma-separated list of question types')

    args = parser.parse_args()

    # Parse question types
    question_types = [t.strip().replace('-', '_') for t in args.types.split(',')]

    # Generate assessment
    result = generate_assessment(args.topic, args.level, args.question_count, question_types)

    # Prepare output
    output = {
        "input": {
            "topic": args.topic,
            "education_level": args.level,
            "question_count": args.question_count,
            "question_types": question_types
        },
        "assessment": result
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()