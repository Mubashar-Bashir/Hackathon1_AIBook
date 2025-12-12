import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import select
from ..models.session import SessionResponse
from ..utils.database import get_db_session
from ..config import settings


class SessionService:
    def __init__(self):
        self.session_timeout_hours = 24 * 7  # 1 week in hours

    def generate_session_token(self) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(32)

    async def create_session(self, user_id: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new session for a user."""
        try:
            from sqlalchemy import select
            from ..utils.database import Base
            from datetime import datetime, timedelta

            # Calculate expiration time (1 week from now)
            expires_at = datetime.utcnow() + timedelta(hours=self.session_timeout_hours)

            async with get_db_session() as db:
                # Create new session
                new_session = Base.classes.sessions(
                    id=secrets.token_urlsafe(16),  # Generate a short ID for the session
                    user_id=user_id,
                    session_token=self.generate_session_token(),
                    expires_at=expires_at,
                    ip_address=ip_address,
                    user_agent=user_agent
                )

                db.add(new_session)
                await db.commit()
                await db.refresh(new_session)

                return {
                    "id": new_session.id,
                    "user_id": new_session.user_id,
                    "session_token": new_session.session_token,
                    "expires_at": new_session.expires_at
                }
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

    async def get_session_by_token(self, token: str) -> Optional[SessionResponse]:
        """Get session information by token."""
        try:
            from sqlalchemy import select
            from ..utils.database import Base
            from datetime import datetime

            async with get_db_session() as db:
                result = await db.execute(
                    select(Base.classes.sessions)
                    .filter_by(session_token=token)
                    .filter(Base.classes.sessions.expires_at > datetime.utcnow())
                )
                session = result.scalars().first()

                if session:
                    return SessionResponse(
                        id=session.id,
                        user_id=session.user_id,
                        session_token=session.session_token,
                        expires_at=session.expires_at,
                        created_at=session.created_at,
                        updated_at=session.updated_at,
                        ip_address=session.ip_address,
                        user_agent=session.user_agent
                    )

            return None
        except Exception as e:
            print(f"Error getting session by token: {e}")
            return None

    async def delete_session(self, token: str) -> bool:
        """Delete a session by token."""
        try:
            from sqlalchemy import delete
            from ..models.session import Session
            from datetime import datetime

            # Get database session using the dependency
            db_gen = get_db_session()
            db = await db_gen.__anext__()  # Get the session from the generator

            try:
                result = await db.execute(
                    delete(Session)
                    .where(Session.session_token == token)
                )
                await db.commit()

                return result.rowcount > 0
            finally:
                # Close the session properly
                await db_gen.aclose()
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    async def validate_session(self, token: str) -> Optional[str]:
        """Validate a session token and return user_id if valid."""
        try:
            from sqlalchemy import select
            from ..utils.database import Base
            from datetime import datetime

            async with get_db_session() as db:
                result = await db.execute(
                    select(Base.classes.sessions)
                    .filter_by(session_token=token)
                    .filter(Base.classes.sessions.expires_at > datetime.utcnow())
                )
                session = result.scalars().first()

                if session:
                    return session.user_id

            return None
        except Exception as e:
            print(f"Error validating session: {e}")
            return None

    async def cleanup_expired_sessions(self) -> int:
        """Remove all expired sessions from the database."""
        try:
            from sqlalchemy import delete
            from ..utils.database import Base
            from datetime import datetime

            async with get_db_session() as db:
                result = await db.execute(
                    delete(Base.classes.sessions)
                    .where(Base.classes.sessions.expires_at < datetime.utcnow())
                )
                await db.commit()

                return result.rowcount
        except Exception as e:
            print(f"Error cleaning up expired sessions: {e}")
            return 0

    async def cleanup_expired_sessions_cron(self, hours_to_keep: int = 24) -> int:
        """Remove expired sessions older than specified hours for maintenance."""
        try:
            from sqlalchemy import delete
            from ..utils.database import Base
            from datetime import datetime, timedelta

            cutoff_time = datetime.utcnow() - timedelta(hours=hours_to_keep)

            async with get_db_session() as db:
                result = await db.execute(
                    delete(Base.classes.sessions)
                    .where(Base.classes.sessions.expires_at < cutoff_time)
                )
                await db.commit()

                return result.rowcount
        except Exception as e:
            print(f"Error cleaning up expired sessions in cron: {e}")
            return 0


# Global instance
session_service = SessionService()