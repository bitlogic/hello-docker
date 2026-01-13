# Unit Testing Guide

This document provides instructions for running and maintaining unit tests for the Flask applications in this Docker tutorial repository.

## Overview

Unit tests have been implemented using Python's `unittest` framework following Test-Driven Development (TDD) principles. The tests cover:

- Flask route functionality
- Redis integration and error handling
- Environment variable configuration
- Edge cases and error scenarios

## Test Locations

Tests are located alongside the application code:

- `1-5-running-docker-compose/app-python/test_app.py`
- `2-building-images/test_app.py`

## Prerequisites

Install testing dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `pytest` - Testing framework
- `pytest-flask` - Flask testing utilities
- `pytest-mock` - Mocking utilities

## Running Tests

### Using unittest (built-in)

Run tests with Python's unittest framework:

```bash
# Run tests for app-python
cd 1-5-running-docker-compose/app-python
python -m unittest test_app.py

# Run tests for building-images
cd 2-building-images
python -m unittest test_app.py
```

### Using pytest (recommended)

Run tests with pytest for better output and features:

```bash
# Run all tests with verbose output
pytest -v

# Run specific test file
pytest 1-5-running-docker-compose/app-python/test_app.py -v

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test class
pytest test_app.py::TestFlaskApp -v

# Run specific test method
pytest test_app.py::TestFlaskApp::test_hello_route_success -v
```

### Running Tests in Docker

You can also run tests inside a Docker container:

```bash
# Build the image with test dependencies
docker build -t flask-app-test -f Dockerfile .

# Run tests in container
docker run --rm flask-app-test python -m unittest test_app.py
```

## Test Structure

### TestFlaskApp Class

Unit tests for individual components:

- `test_hello_route_success` - Tests successful request with working Redis
- `test_hello_route_redis_error` - Tests Redis connection failure handling
- `test_hello_route_default_name` - Tests default environment variable
- `test_hello_route_counter_increments` - Tests counter increment behavior
- `test_hello_route_custom_hostname` - Tests hostname display
- `test_hello_route_special_characters_in_name` - Tests input sanitization
- `test_app_configuration` - Tests Flask app configuration
- `test_redis_connection_parameters` - Tests Redis setup

### TestFlaskAppIntegration Class

Integration tests for end-to-end scenarios:

- `test_multiple_requests_sequence` - Tests multiple sequential requests
- `test_redis_intermittent_failure` - Tests intermittent Redis failures

## Test-Driven Development (TDD) Workflow

Follow these steps when adding new features:

1. **Write the test first** - Define expected behavior
   ```python
   def test_new_feature(self):
       # Arrange
       expected_result = "expected value"
       
       # Act
       result = call_new_feature()
       
       # Assert
       self.assertEqual(result, expected_result)
   ```

2. **Run the test** - It should fail (Red phase)
   ```bash
   pytest test_app.py::TestFlaskApp::test_new_feature
   ```

3. **Implement the feature** - Write minimal code to pass the test (Green phase)

4. **Refactor** - Improve code quality while keeping tests passing

5. **Repeat** for each new feature or bug fix

## Mocking Strategy

Tests use `unittest.mock` to isolate components:

```python
@patch('app.redis')
@patch('app.socket.gethostname')
def test_example(self, mock_hostname, mock_redis):
    # Configure mocks
    mock_redis.incr.return_value = 5
    mock_hostname.return_value = 'test-container'
    
    # Test the application logic
    response = self.client.get('/')
    
    # Verify mock interactions
    mock_redis.incr.assert_called_once_with('counter')
```

## Best Practices

1. **Isolate tests** - Each test should be independent
2. **Use descriptive names** - Test names should explain what they test
3. **Follow AAA pattern** - Arrange, Act, Assert
4. **Mock external dependencies** - Don't rely on actual Redis connections
5. **Test edge cases** - Include error scenarios and boundary conditions
6. **Keep tests fast** - Unit tests should run in milliseconds
7. **Maintain test coverage** - Aim for >80% code coverage

## Continuous Integration

To integrate tests into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest -v --cov=app
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're running tests from the correct directory:

```bash
cd 1-5-running-docker-compose/app-python
python -m unittest test_app.py
```

### Redis Connection Issues

Tests use mocking to avoid actual Redis connections. If you see Redis errors, verify that:

1. Mocks are properly configured with `@patch` decorators
2. The patch path matches the actual import in `app.py`

### Template Not Found

If tests fail with template errors, ensure `templates/hello.html` exists in the same directory as `app.py`.

## Adding New Tests

When adding new functionality to the Flask app:

1. Create a new test method in the appropriate test class
2. Use descriptive names following the pattern: `test_<feature>_<scenario>`
3. Add docstrings explaining what the test validates
4. Follow the Arrange-Act-Assert pattern
5. Run tests to ensure they pass

Example:

```python
def test_new_endpoint_with_valid_input(self):
    """Test new endpoint returns correct response with valid input."""
    # Arrange
    test_data = {'key': 'value'}
    
    # Act
    response = self.client.post('/new-endpoint', json=test_data)
    
    # Assert
    self.assertEqual(response.status_code, 200)
    self.assertIn('expected_key', response.json)
```

## Resources

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [Flask testing guide](https://flask.palletsprojects.com/en/latest/testing/)
- [Test-Driven Development guide](https://testdriven.io/test-driven-development/)

## Support

For questions or issues with tests, please open an issue on the repository or contact the maintainers at [bitlogic](https://bitlogic.io).
