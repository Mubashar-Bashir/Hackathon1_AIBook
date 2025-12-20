#!/usr/bin/env python3
"""
Test script to validate password hashing and verification mechanisms
This addresses task T042: [DEBUG] Validate password hashing and verification mechanisms
"""

import asyncio
import logging
from backend.src.services.auth_service import auth_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_password_security():
    """Test password hashing and verification."""
    logger.info("Starting password security tests...")

    # Test passwords
    test_passwords = [
        "short",  # Should fail length check
        "SecurePassword123!",  # Should pass
        "AnotherSecurePassword456@",  # Should pass
        "",  # Should fail
        "a" * 100  # Very long password
    ]

    all_tests_passed = True

    for i, password in enumerate(test_passwords):
        logger.info(f"Test {i+1}: Testing password '{password[:20]}{'...' if len(password) > 20 else ''}' (length: {len(password)})")

        try:
            # Hash the password
            hashed = auth_service.hash_password(password)
            logger.debug(f"  Hashed: {hashed[:30]}...")

            # Verify the password
            is_valid = auth_service.verify_password(password, hashed)

            if is_valid:
                logger.info(f"  ✅ Password verification successful")
            else:
                logger.error(f"  ❌ Password verification failed")
                all_tests_passed = False

            # Test with wrong password
            wrong_password = password + "wrong"
            is_invalid = not auth_service.verify_password(wrong_password, hashed)

            if is_invalid:
                logger.info(f"  ✅ Correctly rejected wrong password")
            else:
                logger.error(f"  ❌ Incorrectly accepted wrong password")
                all_tests_passed = False

        except Exception as e:
            logger.error(f"  ❌ Error testing password: {e}")
            all_tests_passed = False

    # Test password security properties
    logger.info("Testing password security properties...")

    # Generate multiple hashes for the same password - should be different each time (salt)
    password = "TestPassword123!"
    hash1 = auth_service.hash_password(password)
    hash2 = auth_service.hash_password(password)

    if hash1 != hash2:
        logger.info("✅ Password salting works correctly (different hashes for same password)")
    else:
        logger.error("❌ Password salting failed (same hash for same password)")
        all_tests_passed = False

    # Test verification consistency
    for _ in range(5):
        test_hash = auth_service.hash_password(password)
        if not auth_service.verify_password(password, test_hash):
            logger.error("❌ Password verification is inconsistent")
            all_tests_passed = False
            break

    if all_tests_passed:
        logger.info("✅ All password security tests passed!")
    else:
        logger.error("❌ Some password security tests failed!")

    return all_tests_passed

async def main():
    """Run all password security tests."""
    logger.info("Starting password security validation tests...")

    success = await test_password_security()

    if success:
        print("\n🎉 Password security validation completed successfully!")
        return True
    else:
        print("\n💥 Password security validation failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)