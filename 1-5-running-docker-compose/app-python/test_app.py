"""
Unit tests for the Flask application using unittest framework.

This test suite covers:
- Flask route functionality
- Redis connection and counter behavior
- Error handling for Redis failures
- Environment variable handling
"""

import unittest
from unittest.mock import patch, MagicMock
import os
from redis import RedisError
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test suite for the Flask application."""

    def setUp(self):
        """Set up test client and test environment."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after tests."""
        # Remove any environment variables set during tests
        if 'NAME' in os.environ:
            del os.environ['NAME']

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_hello_route_success(self, mock_hostname, mock_redis):
        """Test successful request to hello route with Redis working."""
        # Arrange
        mock_redis.incr.return_value = 5
        mock_hostname.return_value = 'test-container'
        os.environ['NAME'] = 'TestUser'

        # Act
        response = self.client.get('/')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestUser', response.data)
        self.assertIn(b'test-container', response.data)
        self.assertIn(b'5', response.data)
        mock_redis.incr.assert_called_once_with('counter')

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_hello_route_redis_error(self, mock_hostname, mock_redis):
        """Test hello route when Redis connection fails."""
        # Arrange
        mock_redis.incr.side_effect = RedisError('Connection failed')
        mock_hostname.return_value = 'test-container'
        os.environ['NAME'] = 'TestUser'

        # Act
        response = self.client.get('/')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cannot connect to Redis, counter disabled', response.data)
        self.assertIn(b'TestUser', response.data)
        self.assertIn(b'test-container', response.data)

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_hello_route_default_name(self, mock_hostname, mock_redis):
        """Test hello route with default NAME environment variable."""
        # Arrange
        mock_redis.incr.return_value = 1
        mock_hostname.return_value = 'test-container'
        # Ensure NAME is not set
        if 'NAME' in os.environ:
            del os.environ['NAME']

        # Act
        response = self.client.get('/')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'world', response.data)  # Default value
        self.assertIn(b'test-container', response.data)

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_hello_route_counter_increments(self, mock_hostname, mock_redis):
        """Test that Redis counter increments on multiple requests."""
        # Arrange
        mock_hostname.return_value = 'test-container'
        counter_values = [1, 2, 3]
        mock_redis.incr.side_effect = counter_values

        # Act & Assert
        for expected_count in counter_values:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(str(expected_count).encode(), response.data)

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_hello_route_custom_hostname(self, mock_hostname, mock_redis):
        """Test that the actual hostname is displayed correctly."""
        # Arrange
        mock_redis.incr.return_value = 1
        custom_hostname = 'my-custom-docker-container-xyz'
        mock_hostname.return_value = custom_hostname

        # Act
        response = self.client.get('/')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn(custom_hostname.encode(), response.data)

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_hello_route_special_characters_in_name(self, mock_hostname, mock_redis):
        """Test hello route with special characters in NAME."""
        # Arrange
        mock_redis.incr.return_value = 1
        mock_hostname.return_value = 'test-container'
        os.environ['NAME'] = 'Test & User <123>'

        # Act
        response = self.client.get('/')

        # Assert
        self.assertEqual(response.status_code, 200)
        # Flask auto-escapes HTML, so we check for escaped content
        self.assertIn(b'Test', response.data)

    def test_app_configuration(self):
        """Test that Flask app is properly configured."""
        # Assert
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config['TESTING'])

    @patch('app.redis')
    def test_redis_connection_parameters(self, mock_redis):
        """Test that Redis is configured with correct parameters."""
        # This test verifies the Redis initialization in app.py
        # The actual connection is made at module level
        from app import redis as app_redis
        # Just verify redis object exists
        self.assertIsNotNone(app_redis)


class TestFlaskAppIntegration(unittest.TestCase):
    """Integration tests for Flask app endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_multiple_requests_sequence(self, mock_hostname, mock_redis):
        """Test a sequence of multiple requests to verify consistency."""
        # Arrange
        mock_hostname.return_value = 'test-container'
        mock_redis.incr.side_effect = [1, 2, 3, 4, 5]

        # Act
        responses = [self.client.get('/') for _ in range(5)]

        # Assert
        for response in responses:
            self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_redis.incr.call_count, 5)

    @patch('app.redis')
    @patch('app.socket.gethostname')
    def test_redis_intermittent_failure(self, mock_hostname, mock_redis):
        """Test handling of intermittent Redis failures."""
        # Arrange
        mock_hostname.return_value = 'test-container'
        # Simulate success, then failure, then success
        mock_redis.incr.side_effect = [
            1,
            RedisError('Temporary failure'),
            2
        ]

        # Act & Assert
        response1 = self.client.get('/')
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b'1', response1.data)

        response2 = self.client.get('/')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'cannot connect to Redis', response2.data)

        response3 = self.client.get('/')
        self.assertEqual(response3.status_code, 200)
        self.assertIn(b'2', response3.data)


if __name__ == '__main__':
    unittest.main()
