# Quickstart: Skills and Sub Agents for RI Implementation

## Overview
This guide explains how to use the specialized skills and subagents created to support the Red/Green/Refactor/Implementation phases of the AIBook project.

## Prerequisites
- Claude Code installed and configured
- Access to the AIBook project repository
- Basic understanding of Claude Code skills and subagents

## Available Skills

### 1. UI/UX Design Skill
**Purpose**: Provides expertise in educational interface design and user experience optimization
**When to use**: When working on UI/UX improvements, interface design, or user experience enhancements
**Tools available**: Read, Edit, Grep, WebSearch, WebFetch

### 2. Frontend Development Skill
**Purpose**: Specialized in Docusaurus/React implementation and integration
**When to use**: When implementing frontend features, components, or Docusaurus customizations
**Tools available**: Read, Edit, Write, Grep, Bash, WebSearch

### 3. AI Integration Skill
**Purpose**: Expertise in RAG systems, LLM integration, and AI feature implementation
**When to use**: When working with AI features, RAG implementation, or LLM integrations
**Tools available**: Read, Edit, Grep, Bash, WebSearch, WebFetch

### 4. Backend Development Skill
**Purpose**: Specialized in FastAPI, database, and API design
**When to use**: When implementing backend features, APIs, or database interactions
**Tools available**: Read, Edit, Write, Grep, Bash, WebSearch

### 5. Testing/QA Skill
**Purpose**: Comprehensive testing and quality assurance
**When to use**: When creating tests, performing QA, or validating implementations
**Tools available**: Read, Edit, Grep, Bash, WebSearch

### 6. Accessibility Skill
**Purpose**: WCAG compliance and inclusive design
**When to use**: When ensuring accessibility compliance or implementing inclusive features
**Tools available**: Read, Edit, Grep, WebSearch, WebFetch

## Available Subagents

### 1. UI/UX Expert Agent
**Purpose**: Complex UI/UX design tasks requiring separate context
**When to use**: For comprehensive UI/UX redesigns or complex design challenges

### 2. Frontend Expert Agent
**Purpose**: Complex frontend implementation tasks
**When to use**: For complex React/Docusaurus implementations requiring dedicated focus

### 3. AI/RAG Expert Agent
**Purpose**: Complex AI integration and RAG system tasks
**When to use**: For sophisticated AI feature implementations

### 4. Backend Expert Agent
**Purpose**: Complex backend development tasks
**When to use**: For complex API design or database architecture challenges

### 5. Web Design Optimizer Agent
**Purpose**: Performance and SEO optimization tasks
**When to use**: For optimization challenges requiring dedicated analysis

## Usage Examples

### Automatic Skill Invocation
Claude Code will automatically select appropriate skills based on your requests:
```
"Help me improve the chat interface design"
# Claude Code automatically invokes the UI/UX Design Skill
```

### Manual Subagent Invocation
For complex tasks requiring separate context:
```
"Use the AI/RAG expert subagent to design the complete RAG pipeline"
# Claude Code delegates to the AI/RAG Expert Agent with separate context
```

## Configuration
Skills can be configured per project by modifying their configuration parameters in the respective skill directories.

## Troubleshooting
- If a skill isn't being invoked automatically, try being more specific about the domain in your request
- If a subagent seems unresponsive, check that it has the necessary tool access permissions
- For performance issues, ensure your requests are focused on specific tasks rather than broad questions