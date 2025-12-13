"""
Test configuration for the AIBook authentication system.
This addresses task T009: Create initial test configuration in backend/tests/conftest.py
"""
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.models.user import User
from src.models.session import Session
from src.models.account import Account
from src.models.verification_token import VerificationToken
from src.utils.database import Base
from fastapi.testclient import TestClient
from src.main import app  # Assuming your main FastAPI app is in src.main


# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},  # Required for SQLite
        echo=True  # Enable SQL logging for debugging
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def db_session(db_engine):
    """Create a test database session."""
    async with db_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    async_session_local = sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_local() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
def test_client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def test_user(db_session):
    """Create a test user for authentication tests."""
    from src.services.auth_service import hash_password

    # Create a test user
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password_hash": hash_password("testpassword123"),
        "experience_level": "beginner",
        "is_active": True
    }

    from src.models.user import User
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest.fixture(scope="function")
async def authenticated_client(test_client, test_user):
    """Create an authenticated test client."""
    # Login to get a session token
    login_response = test_client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })

    if login_response.status_code == 200:
        token = login_response.json()["session_token"]
        test_client.headers.update({"Authorization": f"Bearer {token}"})

    return test_client


# Configuration for pytest
def pytest_configure(config):
    """Configure pytest settings."""
    config.addinivalue_line(
        "markers", "auth: marks tests as authentication related"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance related"
    )


def pytest_runtest_setup(item):
    """Called before running each test."""
    # Add any setup logic here if needed
    pass


def pytest_runtest_teardown(item, nextitem):
    """Called after running each test."""
    # Add any teardown logic here if needed
    pass


# Print test configuration info
print("Test configuration loaded for AIBook authentication system")
print("Using in-memory SQLite database for testing")
print("Test fixtures available: event_loop, db_engine, db_session, test_client, test_user, authenticated_client")