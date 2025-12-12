# Data Model: Skills and Sub Agents for RI Implementation

## Overview
This document describes the data structures and entities for the specialized skills and subagents system that supports the Red/Green/Refactor/Implementation phases of the AIBook project.

## Entities

### Skill
A specialized capability that extends Claude Code's functionality with domain-specific expertise and tools.

**Attributes**:
- name: String - The unique identifier for the skill
- description: String - A brief explanation of the skill's purpose and expertise area
- version: String - The version of the skill following semantic versioning
- allowed-tools: Array - List of tools the skill is permitted to use
- expertise-area: String - The domain of knowledge the skill specializes in (e.g., "UI/UX", "AI Integration", "Backend")
- configuration: Object - Configurable parameters that can be adjusted per project

**Validation Rules**:
- name must be unique across all skills
- description must be 10-200 characters
- allowed-tools must be a valid subset of available Claude Code tools
- expertise-area must be from the predefined list of domains

### Subagent
A specialized AI assistant that operates in its own context window with specific system prompts and tool access.

**Attributes**:
- name: String - The unique identifier for the subagent
- description: String - A brief explanation of the subagent's purpose and expertise
- version: String - The version of the subagent following semantic versioning
- tools: Array - List of tools the subagent is permitted to use
- system-prompt: String - The system prompt that defines the subagent's behavior
- expertise-area: String - The domain of knowledge the subagent specializes in
- configuration: Object - Configurable parameters that can be adjusted per project

**Validation Rules**:
- name must be unique across all subagents
- description must be 10-200 characters
- tools must be a valid subset of available Claude Code tools
- system-prompt must be 50-2000 characters
- expertise-area must be from the predefined list of domains

### SkillInvocation
A record of when a skill is invoked by Claude Code.

**Attributes**:
- id: String - Unique identifier for the invocation
- skill-name: String - The name of the skill invoked
- timestamp: DateTime - When the skill was invoked
- context: String - The user request that triggered the skill
- outcome: String - Whether the skill invocation was successful or failed
- duration: Number - The time taken for the skill to complete in seconds

**Validation Rules**:
- timestamp must be in ISO 8601 format
- outcome must be "success" or "failure"
- duration must be a positive number

### SkillSelectionCriteria
The criteria used to determine which skill should be invoked for a given request.

**Attributes**:
- expertise-match-score: Number - Weighted score of how well the skill's expertise matches the request (0-100)
- context-relevance: Number - How relevant the skill is to the current context (0-100)
- user-preference: Number - Weight based on user's preferred skill for this type of request (0-100)
- fallback-allowed: Boolean - Whether this skill can be used as a fallback when primary skills are unavailable

**Validation Rules**:
- All score values must be between 0 and 100
- fallback-allowed must be boolean

## Relationships
- A Skill belongs to one expertise area
- A Subagent belongs to one expertise area
- Multiple SkillInvocation records can reference the same Skill
- Multiple SkillInvocation records can reference the same Subagent