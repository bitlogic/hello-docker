# Quick Start - Running Unit Tests

## For App Python (Docker Compose Section)

```bash
cd 1-5-running-docker-compose/app-python

# Method 1: Using unittest (built-in)
python -m unittest test_app.py

# Method 2: Using pytest (recommended)
pip install -r requirements.txt
pytest -v test_app.py

# Method 3: Verbose with coverage
pytest -v --cov=app --cov-report=term-missing test_app.py
```

## For Building Images Section

```bash
cd 2-building-images

# Method 1: Using unittest (built-in)
python -m unittest test_app.py

# Method 2: Using pytest (recommended)
pip install -r requirements.txt
pytest -v test_app.py
```

## Run All Tests from Root

```bash
# Validate test structure (no dependencies needed)
python3 validate_tests.py

# Run with pytest
pytest -v

# Run specific test
pytest 1-5-running-docker-compose/app-python/test_app.py::TestFlaskApp::test_hello_route_success -v
```

## Docker Method

```bash
# App Python
cd 1-5-running-docker-compose/app-python
docker build -t flask-test -f Dockerfile.test .
docker run --rm flask-test

# Building Images
cd 2-building-images
docker build -t flask-test -f Dockerfile.test .
docker run --rm flask-test
```

## What Gets Tested

✓ Flask route `/` returns 200 OK  
✓ Redis counter increments correctly  
✓ Redis errors are handled gracefully  
✓ Environment variable NAME works (default: "world")  
✓ Hostname is displayed correctly  
✓ Special characters in NAME are sanitized  
✓ Multiple sequential requests work  
✓ Intermittent Redis failures are handled  

## Quick Validation

```bash
# Just check if tests are valid (fast, no dependencies)
python3 validate_tests.py
```

Output should show:
- ✓ Syntax is valid
- ✓ Found 2 test classes
- ✓ Found 10 test methods
- ✓ All required imports present
- ✓ Uses mocking for isolation

## Need Help?

See `TESTING.md` for comprehensive guide including:
- Detailed test descriptions
- TDD workflow
- Best practices
- Troubleshooting
- CI/CD integration
