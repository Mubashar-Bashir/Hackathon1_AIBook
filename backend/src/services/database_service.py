"""
Database Service for RAG System

This module provides database operations for the RAG system including
CRUD operations for chat sessions, messages, and content models.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
import uuid

from src.models.chat import ChatSession, ChatMessage
from src.models.content import BookContent, TextChunk
from src.models.user import User


class DatabaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # Chat Session Operations
    async def create_chat_session(self, user_id: Optional[str] = None, context_type: str = 'full_book',
                                  selected_text: Optional[str] = None) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            user_id=user_id,
            context_type=context_type,
            selected_text=selected_text
        )
        self.db_session.add(session)
        await self.db_session.commit()
        await self.db_session.refresh(session)
        return session

    async def get_chat_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        result = await self.db_session.execute(
            select(ChatSession)
            .options(selectinload(ChatSession.messages))
            .where(ChatSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def update_chat_session(self, session_id: str, **kwargs) -> Optional[ChatSession]:
        """Update a chat session"""
        session = await self.get_chat_session(session_id)
        if session:
            for key, value in kwargs.items():
                setattr(session, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(session)
        return session

    # Chat Message Operations
    async def create_chat_message(self, session_id: str, sender_type: str, content: str,
                                  metadata: Optional[dict] = None) -> ChatMessage:
        """Create a new chat message"""
        message = ChatMessage(
            session_id=session_id,
            sender_type=sender_type,
            content=content,
            metadata=metadata
        )
        self.db_session.add(message)
        await self.db_session.commit()
        await self.db_session.refresh(message)
        return message

    async def get_chat_messages_by_session(self, session_id: str) -> List[ChatMessage]:
        """Get all messages for a session"""
        result = await self.db_session.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.timestamp)
        )
        return result.scalars().all()

    async def get_latest_messages_by_session(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """Get the latest messages for a session"""
        result = await self.db_session.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()

    # Book Content Operations
    async def create_book_content(self, url: str, title: str, content: str,
                                  source_type: str = 'web_page', metadata: Optional[dict] = None) -> BookContent:
        """Create a new book content entry"""
        book_content = BookContent(
            url=url,
            title=title,
            content_text=content,
            source_type=source_type,
            metadata=metadata
        )
        self.db_session.add(book_content)
        await self.db_session.commit()
        await self.db_session.refresh(book_content)
        return book_content

    async def get_book_content_by_url(self, url: str) -> Optional[BookContent]:
        """Get book content by URL"""
        result = await self.db_session.execute(
            select(BookContent).where(BookContent.url == url)
        )
        return result.scalar_one_or_none()

    async def get_book_content_by_id(self, content_id: str) -> Optional[BookContent]:
        """Get book content by ID"""
        result = await self.db_session.execute(
            select(BookContent).where(BookContent.id == content_id)
        )
        return result.scalar_one_or_none()

    async def update_book_content(self, content_id: str, **kwargs) -> Optional[BookContent]:
        """Update book content"""
        content = await self.get_book_content_by_id(content_id)
        if content:
            for key, value in kwargs.items():
                setattr(content, key, value)
            await self.db_session.commit()
            await self.db_session.refresh(content)
        return content

    # Text Chunk Operations
    async def create_text_chunk(self, content_id: str, chunk_text: str, chunk_index: int,
                                token_count: int, embedding_id: Optional[str] = None,
                                metadata: Optional[dict] = None) -> TextChunk:
        """Create a new text chunk"""
        chunk = TextChunk(
            content_id=content_id,
            chunk_text=chunk_text,
            chunk_index=chunk_index,
            token_count=token_count,
            embedding_id=embedding_id,
            metadata=metadata
        )
        self.db_session.add(chunk)
        await self.db_session.commit()
        await self.db_session.refresh(chunk)
        return chunk

    async def get_text_chunks_by_content_id(self, content_id: str) -> List[TextChunk]:
        """Get all text chunks for a content ID"""
        result = await self.db_session.execute(
            select(TextChunk)
            .where(TextChunk.content_id == content_id)
            .order_by(TextChunk.chunk_index)
        )
        return result.scalars().all()

    async def get_text_chunk_by_embedding_id(self, embedding_id: str) -> Optional[TextChunk]:
        """Get a text chunk by its embedding ID"""
        result = await self.db_session.execute(
            select(TextChunk).where(TextChunk.embedding_id == embedding_id)
        )
        return result.scalar_one_or_none()

    async def update_text_chunk_embedding_id(self, chunk_id: str, embedding_id: str) -> Optional[TextChunk]:
        """Update the embedding ID for a text chunk"""
        result = await self.db_session.execute(
            select(TextChunk).where(TextChunk.id == chunk_id)
        )
        chunk = result.scalar_one_or_none()
        if chunk:
            chunk.embedding_id = embedding_id
            await self.db_session.commit()
            await self.db_session.refresh(chunk)
        return chunk

    # User Operations
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        result = await self.db_session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db_session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    # Utility Methods
    async def get_recent_sessions(self, user_id: Optional[str] = None, limit: int = 10) -> List[ChatSession]:
        """Get recent chat sessions, optionally filtered by user"""
        query = select(ChatSession).order_by(ChatSession.updated_at.desc()).limit(limit)
        if user_id:
            query = query.where(ChatSession.user_id == user_id)

        result = await self.db_session.execute(query)
        return result.scalars().all()