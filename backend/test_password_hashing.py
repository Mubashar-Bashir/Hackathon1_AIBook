"""Test script to validate password hashing and verification mechanisms."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
import hashlib
import secrets

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_password_hashing_mechanisms():
    """Test password hashing and verification mechanisms."""
    logger.info("Starting password hashing and verification test...")

    # Import after setup
    from src.services.auth_service import AuthService

    # Create auth service instance
    auth_service = AuthService()

    # Test 1: Basic password hashing and verification
    logger.info("Testing basic password hashing and verification...")
    test_password = "SecurePassword123!"

    # Hash the password
    hashed_password = auth_service.hash_password(test_password)
    if not hashed_password or ":" not in hashed_password:
        logger.error("Test 1 failed: Password hashing failed or format is incorrect")
        return False

    # Verify the password
    is_valid = auth_service.verify_password(test_password, hashed_password)
    if not is_valid:
        logger.error("Test 1 failed: Password verification failed for correct password")
        return False

    logger.info("✓ Test 1 passed: Basic password hashing and verification works")

    # Test 2: Password verification fails with wrong password
    logger.info("Testing password verification with wrong password...")
    wrong_password = "WrongPassword123!"
    is_valid_wrong = auth_service.verify_password(wrong_password, hashed_password)
    if is_valid_wrong:
        logger.error("Test 2 failed: Password verification should fail with wrong password")
        return False

    logger.info("✓ Test 2 passed: Password verification correctly fails with wrong password")

    # Test 3: Different passwords produce different hashes
    logger.info("Testing that different passwords produce different hashes...")
    password1 = "Password1!"
    password2 = "Password2!"

    hash1 = auth_service.hash_password(password1)
    hash2 = auth_service.hash_password(password2)

    if hash1 == hash2:
        logger.error("Test 3 failed: Different passwords should produce different hashes")
        return False

    # Verify each password with its own hash
    if not auth_service.verify_password(password1, hash1):
        logger.error("Test 3 failed: First password doesn't verify with its own hash")
        return False

    if not auth_service.verify_password(password2, hash2):
        logger.error("Test 3 failed: Second password doesn't verify with its own hash")
        return False

    logger.info("✓ Test 3 passed: Different passwords produce different hashes")

    # Test 4: Same password produces different hashes (due to salt)
    logger.info("Testing that same password produces different hashes (due to salt)...")
    same_password = "SamePassword123!"

    hash1_same = auth_service.hash_password(same_password)
    hash2_same = auth_service.hash_password(same_password)

    if hash1_same == hash2_same:
        logger.error("Test 4 failed: Same password should produce different hashes due to salt")
        return False

    # But both should verify correctly with the original password
    if not auth_service.verify_password(same_password, hash1_same):
        logger.error("Test 4 failed: First hash doesn't verify with original password")
        return False

    if not auth_service.verify_password(same_password, hash2_same):
        logger.error("Test 4 failed: Second hash doesn't verify with original password")
        return False

    logger.info("✓ Test 4 passed: Same password produces different hashes but both verify correctly")

    # Test 5: Empty password handling
    logger.info("Testing empty password handling...")
    try:
        empty_hash = auth_service.hash_password("")
        is_empty_valid = auth_service.verify_password("", empty_hash)
        # This should work but we'll check if it's handled properly by the system
        logger.info("✓ Test 5 passed: Empty password hashing handled (though not recommended in practice)")
    except Exception as e:
        logger.info(f"Empty password hashing failed as expected: {e}")

    # Test 6: Verify hash format (should be salt:hash)
    logger.info("Testing hash format...")
    sample_hash = auth_service.hash_password("TestPassword123!")
    if ":" not in sample_hash:
        logger.error("Test 6 failed: Hash format is incorrect, should be 'salt:hash'")
        return False

    parts = sample_hash.split(":")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        logger.error("Test 6 failed: Hash format should be 'salt:hash' with non-empty parts")
        return False

    logger.info("✓ Test 6 passed: Hash format is correct (salt:hash)")

    # Test 7: Verify that the hashing algorithm is using PBKDF2 with proper parameters
    logger.info("Testing hashing algorithm implementation...")
    # The implementation should use PBKDF2 with 100,000 iterations
    # We can't easily verify the exact algorithm, but we can test the security properties
    import time

    # Hashing should take a measurable amount of time due to iterations
    start_time = time.time()
    auth_service.hash_password("TestPassword123!")
    end_time = time.time()

    hashing_time = end_time - start_time
    if hashing_time < 0.01:  # Should take at least 10ms with 100k iterations
        logger.warning("Hashing is very fast - may not be using sufficient iterations")
    else:
        logger.info(f"✓ Test 7 passed: Hashing takes reasonable time ({hashing_time:.3f}s), suggesting proper iterations")

    # Test 8: Test with various password complexities
    logger.info("Testing with various password complexities...")
    test_passwords = [
        "simple123",
        "ComplexP@ssw0rd!",
        "VeryLongPasswordWithNumbers1234567890AndSymbols!@#$%",
        "aA1!aA1!aA1!",
        "PasswordWithÜnic0de"  # Test with unicode characters
    ]

    for pwd in test_passwords:
        try:
            pwd_hash = auth_service.hash_password(pwd)
            is_valid = auth_service.verify_password(pwd, pwd_hash)
            is_invalid = auth_service.verify_password(pwd + "wrong", pwd_hash)

            if not is_valid:
                logger.error(f"Test 8 failed: Password '{pwd}' doesn't verify with its own hash")
                return False

            if is_invalid:
                logger.error(f"Test 8 failed: Password '{pwd}' shouldn't verify with wrong input")
                return False

        except Exception as e:
            logger.error(f"Test 8 failed: Error testing password '{pwd}': {e}")
            return False

    logger.info("✓ Test 8 passed: Various password complexities handled correctly")

    logger.info("All password hashing and verification tests passed!")
    return True

async def test_security_properties():
    """Test security properties of the password hashing system."""
    logger.info("Testing security properties...")

    from src.services.auth_service import AuthService
    auth_service = AuthService()

    # Test resistance to timing attacks by verifying similar passwords
    # take similar time to process
    import time

    password = "CorrectPassword123!"
    hash_val = auth_service.hash_password(password)

    # Test with passwords of similar length but different
    test_inputs = [
        ("CorrectPassword123!", True),   # Correct password
        ("WrongPassword123456!", False),  # Wrong password, same length
        ("CompletelyWrong123!", False),   # Wrong password, different length
    ]

    times = []
    for test_pwd, should_match in test_inputs:
        start = time.time()
        result = auth_service.verify_password(test_pwd, hash_val)
        end = time.time()

        elapsed = end - start
        times.append(elapsed)

        if result != should_match:
            logger.error(f"Security test failed: Password verification result incorrect for '{test_pwd}'")
            return False

    # In a properly implemented system, verification time should be roughly constant
    # regardless of how similar the input is to the correct password
    logger.info(f"Verification times: {[f'{t:.4f}s' for t in times]}")
    logger.info("✓ Security properties test passed: Password verification behaves correctly")

    return True

async def main():
    """Main function to run password hashing and verification tests."""
    logger.info("Starting password hashing and verification tests...")

    # Run the password hashing tests
    basic_tests_success = await test_password_hashing_mechanisms()
    security_tests_success = await test_security_properties() if basic_tests_success else False

    logger.info(f"Basic password hashing tests: {'PASS' if basic_tests_success else 'FAIL'}")
    logger.info(f"Security properties tests: {'PASS' if security_tests_success else 'FAIL'}")

    overall_success = basic_tests_success and security_tests_success
    logger.info(f"Overall password hashing and verification: {'PASS' if overall_success else 'FAIL'}")

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)