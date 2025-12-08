import google.generativeai as genai
from typing import List, Dict, Optional, Any
from ..config import settings
from ..models.personalization import ApplyPersonalizationRequest, ApplyPersonalizationResponse
from datetime import datetime
import uuid

class PersonalizationService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model_name)

    def _create_personalization_prompt(self, content: str, background: str, personalization_type: str) -> str:
        """Create a prompt for personalizing content based on user background."""
        background_descriptions = {
            "beginner": "someone who is new to this topic and needs simple explanations with basic terminology",
            "intermediate": "someone with some experience in this topic who needs moderate detail and practical examples",
            "expert": "someone with extensive knowledge of this topic who needs advanced explanations and detailed technical information"
        }

        background_desc = background_descriptions.get(background, background_descriptions["intermediate"])

        if personalization_type == "simplification":
            prompt = f"""
            Simplify the following content for {background_desc}. Make it easier to understand:
            {content}
            """
        elif personalization_type == "elaboration":
            prompt = f"""
            Elaborate on the following content for {background_desc}. Add more detail and depth:
            {content}
            """
        elif personalization_type == "examples":
            prompt = f"""
            Enhance the following content for {background_desc} by adding relevant examples and practical applications:
            {content}
            """
        else:  # "all" or default
            prompt = f"""
            Personalize the following content for {background_desc}.
            Adjust complexity, add relevant examples, and ensure the explanation matches their experience level:
            {content}
            """

        return prompt

    async def apply_personalization(self, request: ApplyPersonalizationRequest) -> Optional[ApplyPersonalizationResponse]:
        """Apply personalization to content based on user background."""
        try:
            # Validate background level
            valid_backgrounds = ["beginner", "intermediate", "expert"]
            if request.user_background and request.user_background not in valid_backgrounds:
                raise ValueError(f"Invalid background level: {request.user_background}")

            # Determine the personalization type
            personalization_type = request.personalization_type or "all"

            # Create the personalization prompt
            prompt = self._create_personalization_prompt(
                content=request.content,
                background=request.user_background or "intermediate",  # Default to intermediate
                personalization_type=personalization_type
            )

            # Generate personalized content using Gemini
            response = self.model.generate_content(prompt)

            if not response.text:
                return None

            return ApplyPersonalizationResponse(
                original_content=request.content,
                personalized_content=response.text,
                user_background=request.user_background or "intermediate",
                personalization_type=personalization_type,
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            print(f"Error in personalization service: {e}")
            return None

    async def get_personalized_chapter(self, chapter_id: str, user_background: str) -> Optional[Dict[str, Any]]:
        """Get a personalized version of a chapter based on user background."""
        try:
            # This would typically fetch the original chapter content from storage
            # For now, we'll simulate with a placeholder
            # In a real implementation, this would come from the textbook content storage
            original_content = f"Original content for chapter {chapter_id}"
            original_title = f"Chapter {chapter_id}"

            # Personalize the content
            personalization_request = ApplyPersonalizationRequest(
                content=original_content,
                user_background=user_background,
                personalization_type="all"
            )

            personalization_result = await self.apply_personalization(personalization_request)

            if not personalization_result:
                return None

            return {
                "chapter_id": chapter_id,
                "original_title": original_title,
                "original_content": original_content,
                "personalized_title": f"{original_title} (Personalized for {user_background})",
                "personalized_content": personalization_result.personalized_content,
                "background_level": user_background,
                "personalization_applied": True,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            print(f"Error getting personalized chapter: {e}")
            return None

    async def store_personalization(self, chapter_id: str, user_background: str, personalized_content: str) -> bool:
        """Store personalized content for future use."""
        # In a real implementation, this would store the personalized content in a database
        # For now, we'll just return True to indicate success
        try:
            # This would typically insert into a personalizations table
            # Implementation would depend on the database schema
            return True
        except Exception as e:
            print(f"Error storing personalization: {e}")
            return False

# Global instance
personalization_service = PersonalizationService()