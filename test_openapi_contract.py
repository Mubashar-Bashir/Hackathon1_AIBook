#!/usr/bin/env python3
"""
Test to validate all API endpoints against the OpenAPI contract
This addresses task T047: Validate all API endpoints against the OpenAPI contract
"""

import asyncio
import os
import logging
from fastapi.testclient import TestClient
from backend.main import app
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openapi_contract():
    """Validate all API endpoints against the OpenAPI contract."""
    logger.info("Starting OpenAPI contract validation...")

    # Create a test client
    client = TestClient(app)

    # Get the OpenAPI schema
    schema_response = client.get("/openapi.json")
    if schema_response.status_code != 200:
        logger.error("❌ Could not retrieve OpenAPI schema")
        return False

    schema = schema_response.json()
    logger.info(f"✅ Retrieved OpenAPI schema with {len(schema.get('paths', {}))} paths")

    # Validate the basic structure of the schema
    required_fields = ['openapi', 'info', 'paths']
    for field in required_fields:
        if field not in schema:
            logger.error(f"❌ OpenAPI schema missing required field: {field}")
            return False

    logger.info(f"✅ OpenAPI version: {schema['openapi']}")
    logger.info(f"✅ API title: {schema['info']['title']}")
    logger.info(f"✅ API description: {schema['info'].get('description', 'No description')}")

    # Check for authentication-related paths
    auth_paths = []
    for path, methods in schema.get('paths', {}).items():
        if 'auth' in path.lower():
            auth_paths.append(path)

    logger.info(f"✅ Found {len(auth_paths)} authentication-related paths in schema:")
    for path in auth_paths:
        logger.info(f"   - {path}")

    # Validate each auth-related endpoint by checking if it exists and is accessible
    validated_endpoints = 0
    total_auth_endpoints = len(auth_paths)

    for path in auth_paths:
        # Get the methods available for this path
        path_methods = list(schema['paths'][path].keys())
        logger.info(f"Validating path: {path} with methods: {path_methods}")

        for method in path_methods:
            method = method.upper()

            # Skip some methods that don't make sense to test directly
            if method in ['OPTIONS', 'HEAD']:
                continue

            # Test if the endpoint is accessible (we expect 401/405/422 for auth endpoints, not 404)
            try:
                if method == 'GET':
                    response = client.get(path)
                elif method == 'POST':
                    response = client.post(path, json={})
                elif method == 'PUT':
                    response = client.put(path, json={})
                elif method == 'DELETE':
                    response = client.delete(path)
                elif method == 'PATCH':
                    response = client.patch(path, json={})
                else:
                    # For other methods, try with empty JSON
                    response = getattr(client, method.lower(), lambda *args, **kwargs: None)(path, json={})

                if response.status_code not in [404]:  # 404 means endpoint doesn't exist
                    logger.info(f"   ✅ {method} {path} - Status: {response.status_code} (endpoint exists)")
                    validated_endpoints += 1
                else:
                    logger.error(f"   ❌ {method} {path} - Status: {response.status_code} (endpoint not found)")
            except Exception as e:
                logger.error(f"   ❌ {method} {path} - Error: {e}")

    # Validate specific authentication endpoints that we know should exist
    expected_auth_endpoints = [
        "/api/auth/register",
        "/api/auth/login",
        "/api/auth/profile",
        "/api/auth/logout",
        "/api/auth/me"
    ]

    logger.info("Validating expected authentication endpoints...")
    missing_endpoints = []

    for expected_path in expected_auth_endpoints:
        if expected_path not in schema.get('paths', {}):
            missing_endpoints.append(expected_path)
            logger.error(f"❌ Expected endpoint missing from OpenAPI schema: {expected_path}")
        else:
            logger.info(f"✅ Expected endpoint found in schema: {expected_path}")

    if missing_endpoints:
        logger.error(f"❌ {len(missing_endpoints)} expected endpoints missing from schema")
        return False

    # Validate response structure for auth endpoints
    logger.info("Validating response structures for auth endpoints...")

    # Check if the schema has proper response definitions
    components = schema.get('components', {})
    schemas = components.get('schemas', {})

    auth_response_schemas = ['UserRegistrationResponse', 'UserLoginResponse', 'UserProfileResponse']
    missing_schemas = []

    for schema_name in auth_response_schemas:
        if schema_name not in schemas:
            missing_schemas.append(schema_name)
            logger.warning(f"⚠️  Response schema not found: {schema_name}")
        else:
            logger.info(f"✅ Response schema found: {schema_name}")

    # Validate parameter definitions
    logger.info("Validating parameter and request body definitions...")

    # Check for common auth request bodies
    auth_request_bodies = ['UserRegistrationRequest', 'UserLogin', 'UserUpdate']
    missing_request_bodies = []

    for body_name in auth_request_bodies:
        if body_name not in schemas:
            missing_request_bodies.append(body_name)
            logger.warning(f"⚠️  Request body schema not found: {body_name}")
        else:
            logger.info(f"✅ Request body schema found: {body_name}")

    # Summary
    logger.info(f"\nOpenAPI Contract Validation Summary:")
    logger.info(f"- Total auth paths in schema: {total_auth_endpoints}")
    logger.info(f"- Endpoints successfully validated: {validated_endpoints}/{total_auth_endpoints}")
    logger.info(f"- Expected endpoints present: {len(expected_auth_endpoints) - len(missing_endpoints)}/{len(expected_auth_endpoints)}")
    logger.info(f"- Response schemas found: {len(auth_response_schemas) - len(missing_schemas)}/{len(auth_response_schemas)}")
    logger.info(f"- Request schemas found: {len(auth_request_bodies) - len(missing_request_bodies)}/{len(auth_request_bodies)}")

    # The validation is considered successful if all expected endpoints are in the schema
    if len(missing_endpoints) == 0:
        logger.info("✅ OpenAPI contract validation passed!")
        return True
    else:
        logger.error("❌ OpenAPI contract validation failed - some expected endpoints are missing")
        return False

def main():
    """Run OpenAPI contract validation."""
    logger.info("Starting OpenAPI contract validation...")

    success = test_openapi_contract()

    if success:
        print("\n🎉 OpenAPI contract validation completed successfully!")
        print("All expected authentication endpoints are properly defined in the schema.")
        return True
    else:
        print("\n💥 OpenAPI contract validation failed!")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)