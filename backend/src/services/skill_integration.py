"""
Skill Integration Module

This module provides integration between the existing RAG functionality
and the new skills/agents architecture.
"""

from typing import Dict, Any, Optional, List
import subprocess
import json
import os
from ..services.rag_service import rag_service
from ..models.chatbot import ChatbotQueryResponse


class SkillIntegrationService:
    def __init__(self):
        self.rag_service = rag_service
        self.skills_base_path = ".claude/skills"

    def execute_rag_query_skill(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Execute the RAG query skill using the existing RAG service.
        """
        try:
            # Use the existing RAG service to process the query
            result = self.rag_service.process_query_with_enhanced_reasoning(
                query=query,
                context_type="full_book"
            )

            if result:
                return {
                    "response": result.response,
                    "sources": result.sources,
                    "confidence": result.confidence,
                    "query_embedding": [0.0] * 1536  # Placeholder for actual embedding
                }
            else:
                return {
                    "response": "No response generated",
                    "sources": [],
                    "confidence": 0.0,
                    "query_embedding": [0.0] * 1536
                }
        except Exception as e:
            print(f"Error executing RAG query skill: {e}")
            return {
                "response": f"Error executing RAG query: {str(e)}",
                "sources": [],
                "confidence": 0.0,
                "query_embedding": [0.0] * 1536
            }

    def execute_content_navigation_skill(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Execute the content navigation skill to find specific content in the textbook.
        """
        try:
            # Use the embedding service to find relevant content
            from ..services.embedding_service import embedding_service
            search_results = embedding_service.search_similar_content(query, max_results)

            results = []
            if search_results:
                for result in search_results:
                    results.append({
                        "title": result.get("title", "Unknown Title"),
                        "type": "section",
                        "path": result.get("content_id", ""),
                        "relevance_score": result.get("similarity", 0.0)
                    })

            return {
                "query": query,
                "results": results,
                "total_found": len(results)
            }
        except Exception as e:
            print(f"Error executing content navigation skill: {e}")
            return {
                "query": query,
                "results": [],
                "total_found": 0
            }

    def execute_skill_by_name(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a skill by its name with provided arguments.
        """
        if skill_name.lower() == "ragqueryskill":
            query = kwargs.get('query', '')
            top_k = kwargs.get('top_k', 5)
            return self.execute_rag_query_skill(query, top_k)
        elif skill_name.lower() == "contentnavigationskill":
            query = kwargs.get('query', '')
            max_results = kwargs.get('max_results', 5)
            return self.execute_content_navigation_skill(query, max_results)
        else:
            return {
                "error": f"Skill '{skill_name}' not found or not implemented",
                "available_skills": ["RAGQuerySkill", "ContentNavigationSkill"]
            }

    def get_authorized_skills_for_agent(self, agent_name: str) -> List[Dict[str, str]]:
        """
        Get the list of authorized skills for a specific agent.
        """
        # For now, return a default set of skills for the textbook expert agent
        if agent_name.lower() == "textbookexpertagent":
            return [
                {
                    "name": "RAGQuerySkill",
                    "path": f"{self.skills_base_path}/rag_query",
                    "description": "For semantic search and question answering from textbook content"
                },
                {
                    "name": "ContentNavigationSkill",
                    "path": f"{self.skills_base_path}/content_navigation",
                    "description": "For finding specific chapters, sections, and content locations"
                }
            ]
        else:
            return []

    def execute_agent_with_skills(self, agent_name: str, query: str) -> Dict[str, Any]:
        """
        Execute an agent with its authorized skills.
        """
        try:
            authorized_skills = self.get_authorized_skills_for_agent(agent_name)

            if not authorized_skills:
                return {
                    "error": f"No authorized skills found for agent '{agent_name}'",
                    "response": f"I'm the {agent_name} but I don't have any authorized skills to help with your query."
                }

            # For the textbook expert agent, use the RAG query skill as the primary approach
            if agent_name.lower() == "textbookexpertagent":
                rag_result = self.execute_rag_query_skill(query)

                return {
                    "agent": agent_name,
                    "response": rag_result["response"],
                    "sources": rag_result["sources"],
                    "confidence": rag_result["confidence"],
                    "skills_used": ["RAGQuerySkill"],
                    "query": query
                }
            else:
                return {
                    "error": f"Agent '{agent_name}' not implemented",
                    "response": f"I'm sorry, the agent '{agent_name}' is not fully implemented yet."
                }

        except Exception as e:
            print(f"Error executing agent '{agent_name}': {e}")
            return {
                "error": str(e),
                "response": f"Error executing agent: {str(e)}"
            }


# Global instance
skill_integration_service = SkillIntegrationService()