import pytest
from src.middleware.validation import InputValidator, validate_and_sanitize_input, validate_email_input, validate_password_input


class TestInputValidator:
    @pytest.fixture
    def validator(self):
        """Create a validator instance for testing."""
        return InputValidator()

    def test_email_validation(self, validator):
        """Test email validation."""
        # Valid emails
        assert validator.validate_email("test@example.com") is True
        assert validator.validate_email("user.name+tag@example.co.uk") is True
        assert validator.validate_email("user@sub.domain.org") is True

        # Invalid emails
        assert validator.validate_email("invalid-email") is False
        assert validator.validate_email("@example.com") is False
        assert validator.validate_email("test@") is False
        assert validator.validate_email("test.example.com") is False

    def test_url_validation(self, validator):
        """Test URL validation."""
        # Valid URLs
        assert validator.validate_url("https://example.com") is True
        assert validator.validate_url("http://localhost:8000") is True
        assert validator.validate_url("https://sub.domain.co.uk/path") is True

        # Invalid URLs
        assert validator.validate_url("not-a-url") is False
        assert validator.validate_url("ftp://example.com") is False
        assert validator.validate_url("javascript:alert('xss')") is False

    def test_username_validation(self, validator):
        """Test username validation."""
        # Valid usernames
        assert validator.validate_username("user123") is True
        assert validator.validate_username("test_user") is True
        assert validator.validate_username("a1b2c3d4e5f6g7h8i9j0") is True  # 20 chars

        # Invalid usernames
        assert validator.validate_username("us") is False  # Too short
        assert validator.validate_username("a1b2c3d4e5f6g7h8i9j0k") is False  # Too long
        assert validator.validate_username("user@name") is False  # Invalid character
        assert validator.validate_username("user name") is False  # Space not allowed

    def test_password_validation(self, validator):
        """Test password validation."""
        # Valid passwords
        assert validator.validate_password("password123") is True
        assert validator.validate_password("SecurePass123!") is True

        # Invalid passwords
        assert validator.validate_password("password") is False  # No number
        assert validator.validate_password("12345678") is False  # No letter
        assert validator.validate_password("pass") is False  # Too short
        assert validator.validate_password("123") is False  # Too short, no letter

    def test_text_sanitization(self, validator):
        """Test text sanitization."""
        # Test basic sanitization
        input_text = "This is a test <script>alert('xss')</script> string"
        sanitized = validator.sanitize_text(input_text)
        assert "<script>" not in sanitized
        assert "alert('xss')" not in sanitized
        assert "This is a test" in sanitized

        # Test length limiting
        long_text = "a" * 1005  # More than default max length of 10000
        sanitized = validator.sanitize_text(long_text, max_length=1000)
        assert len(sanitized) <= 1000

        # Test URL decoding
        encoded_text = "Hello%20World"
        sanitized = validator.sanitize_text(encoded_text)
        assert "Hello World" in sanitized

        # Test removal of javascript: URLs
        js_text = "Click here javascript:alert('xss')"
        sanitized = validator.sanitize_text(js_text)
        assert "javascript:" not in sanitized

    def test_json_depth_validation(self, validator):
        """Test JSON depth validation."""
        # Valid: shallow nesting
        shallow_obj = {"level1": {"level2": "value"}}
        assert validator.validate_json_depth(shallow_obj, max_depth=5) is True

        # Valid: within limit
        nested_obj = {"l1": {"l2": {"l3": {"l4": {"l5": "value"}}}}}
        assert validator.validate_json_depth(nested_obj, max_depth=5) is True

        # Invalid: too deep
        too_deep_obj = {"l1": {"l2": {"l3": {"l4": {"l5": {"l6": "value"}}}}}}
        assert validator.validate_json_depth(too_deep_obj, max_depth=5) is False


class TestValidationFunctions:
    def test_validate_and_sanitize_input(self):
        """Test the validation and sanitization function."""
        # Test normal input
        result = validate_and_sanitize_input("Hello World")
        assert result == "Hello World"

        # Test with XSS attempt
        xss_input = "<script>alert('xss')</script>Hello"
        result = validate_and_sanitize_input(xss_input)
        assert "<script>" not in result

        # Test with None input
        result = validate_and_sanitize_input(None)
        assert result == ""

        # Test length limit
        long_input = "a" * 1500
        result = validate_and_sanitize_input(long_input, max_length=1000)
        assert len(result) <= 1000

    def test_validate_email_input(self):
        """Test email validation function."""
        # Valid email
        result = validate_email_input("test@example.com")
        assert result == "test@example.com"

        # Invalid email should raise exception
        with pytest.raises(Exception):
            validate_email_input("invalid-email")

    def test_validate_password_input(self):
        """Test password validation function."""
        # Valid password
        result = validate_password_input("password123")
        assert result == "password123"

        # Invalid password should raise exception
        with pytest.raises(Exception):
            validate_password_input("weak")