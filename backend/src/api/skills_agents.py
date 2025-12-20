"""
Skills and Agents API

API endpoints for interacting with skills and agents.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..services.skill_integration import skill_integration_service


router = APIRouter()


class SkillExecutionRequest(BaseModel):
    skill_name: str
    parameters: Dict[str, Any]


class AgentExecutionRequest(BaseModel):
    agent_name: str
    query: str
    parameters: Optional[Dict[str, Any]] = {}


@router.post("/skills/execute")
async def execute_skill(request: SkillExecutionRequest):
    """
    Execute a specific skill with given parameters.
    """
    try:
        result = skill_integration_service.execute_skill_by_name(
            request.skill_name,
            **request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing skill: {str(e)}")


@router.post("/agents/execute")
async def execute_agent(request: AgentExecutionRequest):
    """
    Execute a specific agent with a query and parameters.
    """
    try:
        result = skill_integration_service.execute_agent_with_skills(
            request.agent_name,
            request.query
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")


@router.get("/skills/list")
async def list_skills():
    """
    List available skills with their descriptions.
    """
    return {
        "skills": [
            {
                "name": "RAGQuerySkill",
                "description": "Performs semantic search and retrieval-augmented generation using vector embeddings to answer questions based on the Physical AI & Humanoid Robotics textbook content."
            },
            {
                "name": "ContentNavigationSkill",
                "description": "Helps users find specific chapters, sections, or content within the Physical AI & Humanoid Robotics textbook."
            }
        ]
    }


@router.get("/agents/list")
async def list_agents():
    """
    List available agents with their descriptions.
    """
    return {
        "agents": [
            {
                "name": "TextbookExpertAgent",
                "description": "Specializes in answering questions about the Physical AI & Humanoid Robotics textbook content, providing detailed explanations and references to specific chapters.",
                "capabilities": ["textbook Q&A", "content retrieval", "educational explanations", "chapter referencing"]
            }
        ]
    }


@router.post("/skills/rag-query")
async def rag_query_skill(query: str = Query(..., description="The query to search for"),
                          top_k: int = Query(5, description="Number of results to retrieve")):
    """
    Execute the RAG query skill directly.
    """
    try:
        result = skill_integration_service.execute_rag_query_skill(query, top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing RAG query skill: {str(e)}")


@router.post("/skills/content-navigation")
async def content_navigation_skill(query: str = Query(..., description="The content to search for"),
                                   max_results: int = Query(5, description="Maximum number of results to return")):
    """
    Execute the content navigation skill directly.
    """
    try:
        result = skill_integration_service.execute_content_navigation_skill(query, max_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing content navigation skill: {str(e)}")