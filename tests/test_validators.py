"""Unit tests for validators."""

import unittest
from backend.utils.validators import (
    validate_confidence_threshold,
    validate_session_id
)


class TestValidators(unittest.TestCase):
    """Test cases for validation utilities."""

    def test_valid_confidence_threshold(self):
        """Test valid confidence threshold."""
        result = validate_confidence_threshold(0.7)
        self.assertTrue(result['valid'])
        self.assertEqual(result['value'], 0.7)

    def test_invalid_confidence_threshold_range(self):
        """Test confidence threshold out of range."""
        result = validate_confidence_threshold(1.5)
        self.assertFalse(result['valid'])

    def test_valid_session_id(self):
        """Test valid session ID."""
        result = validate_session_id('test-session-123')
        self.assertTrue(result['valid'])

    def test_invalid_session_id(self):
        """Test invalid session ID."""
        result = validate_session_id('invalid@session!')
        self.assertFalse(result['valid'])


if __name__ == '__main__':
    unittest.main()
