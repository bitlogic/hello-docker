#!/usr/bin/env python3
"""
Test validation script - Checks test files for syntax errors and structure.
"""

import ast
import sys
from pathlib import Path


def validate_test_file(filepath):
    """Validate a Python test file for syntax and structure."""
    print(f"\n{'='*60}")
    print(f"Validating: {filepath}")
    print('='*60)
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse the file to check for syntax errors
        tree = ast.parse(content)
        print("✓ Syntax is valid")
        
        # Check for test classes
        test_classes = [node for node in ast.walk(tree) 
                       if isinstance(node, ast.ClassDef) 
                       and node.name.startswith('Test')]
        print(f"✓ Found {len(test_classes)} test class(es):")
        for cls in test_classes:
            print(f"  - {cls.name}")
        
        # Check for test methods
        test_methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                test_methods.append(node.name)
        
        print(f"✓ Found {len(test_methods)} test method(s):")
        for i, method in enumerate(test_methods[:10], 1):  # Show first 10
            print(f"  {i}. {method}")
        if len(test_methods) > 10:
            print(f"  ... and {len(test_methods) - 10} more")
        
        # Check for imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        required_imports = ['unittest', 'app']
        missing = [imp for imp in required_imports if imp not in imports]
        
        if not missing:
            print(f"✓ All required imports present")
        else:
            print(f"⚠ Missing imports: {missing}")
        
        # Check for docstrings
        docstring_count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    docstring_count += 1
        
        print(f"✓ {docstring_count} functions/classes have docstrings")
        
        # Check for mock usage
        has_mock = 'mock' in content.lower() or '@patch' in content
        if has_mock:
            print("✓ Uses mocking for isolation")
        else:
            print("⚠ No mocking detected (may depend on external services)")
        
        return True
        
    except SyntaxError as e:
        print(f"✗ Syntax Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Main validation function."""
    test_files = [
        "1-5-running-docker-compose/app-python/test_app.py",
        "2-building-images/test_app.py"
    ]
    
    all_valid = True
    for test_file in test_files:
        filepath = Path(test_file)
        if not filepath.exists():
            print(f"\n✗ File not found: {test_file}")
            all_valid = False
            continue
        
        if not validate_test_file(filepath):
            all_valid = False
    
    print(f"\n{'='*60}")
    if all_valid:
        print("✓ All test files are valid and well-structured!")
        print('='*60)
        return 0
    else:
        print("✗ Some test files have issues")
        print('='*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
