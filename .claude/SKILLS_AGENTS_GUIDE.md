# Skills and Agents Usage Guide

## Overview

This project implements a skills and agents architecture following the AIDD (Agent IDD) framework. Skills provide specific capabilities while agents coordinate these skills to accomplish complex tasks.

## Skills Structure

Skills are located in the `.claude/skills/` directory and follow this structure:

```
.claude/skills/
├── skill_name/
│   ├── skill_metadata.json      # Skill identification and discovery
│   ├── skill_instructions.md    # Core operational instructions
│   ├── scripts/                 # Executable code for the skill
│   └── assets/                  # Supporting files and configurations
└── SKILL_TEMPLATE.md            # Template for creating new skills
```

### Creating a New Skill

1. Create a new directory in `.claude/skills/`
2. Add `skill_metadata.json` with name, version, keywords, and description
3. Add `skill_instructions.md` with procedural steps and usage guidelines
4. Add any necessary scripts to the `scripts/` directory
5. Add any supporting files to the `assets/` directory

## Agents Structure

Agents are located in the `.claude/agents/` directory and follow this structure:

```
.claude/agents/
├── agent_name/
│   ├── agent_metadata.json      # Agent identification and discovery
│   ├── agent_instructions.md    # Core role and operational guidelines
│   ├── skills/                  # Authorized skills for this agent
│   ├── scripts/                 # Agent-specific executable code
│   └── assets/                  # Agent configurations and data
└── AGENT_TEMPLATE.md            # Template for creating new agents
```

### Creating a New Agent

1. Create a new directory in `.claude/agents/`
2. Add `agent_metadata.json` with name, version, keywords, and description
3. Add `agent_instructions.md` with role definition and operational guidelines
4. Define authorized skills in `assets/authorized_skills.json`
5. Add any necessary scripts to the `scripts/` directory

## Available Skills

### RAGQuerySkill
- **Purpose**: Performs semantic search and retrieval-augmented generation
- **Keywords**: RAG, query, search, vector, retrieval, augmented generation
- **Usage**: Query the textbook content using semantic search

### ContentNavigationSkill
- **Purpose**: Helps find specific chapters, sections, or content
- **Keywords**: navigation, table of contents, chapter, section
- **Usage**: Locate specific content within the textbook

## Available Agents

### TextbookExpertAgent
- **Purpose**: Educational assistant for the Physical AI & Humanoid Robotics textbook
- **Keywords**: textbook, expert, education, learning, Q&A
- **Capabilities**: textbook Q&A, content retrieval, educational explanations

## Using Skills Programmatically

Skills can be invoked programmatically by executing their scripts:

```bash
# Example: Using the RAG query skill
python .claude/skills/rag_query/scripts/rag_query.py --query "What is Physical AI?" --top_k 3

# Example: Using the content navigation skill
python .claude/skills/content_navigation/scripts/content_navigation.py --query "humanoid control" --max_results 3
```

## Agent Authorization

Agents can only use skills that are explicitly listed in their `authorized_skills.json` file. This provides security and ensures proper role boundaries.

## Best Practices

1. **Modularity**: Keep skills focused on a single capability
2. **Documentation**: Maintain clear instructions in skill/agent markdown files
3. **Versioning**: Update version numbers when making changes
4. **Testing**: Test skills and agents in isolation before integration
5. **Security**: Only authorize necessary skills for each agent