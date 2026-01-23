#!/usr/bin/env python3
"""
Test script to validate CSV import functionality without Docker.
This script tests the core CSV validation and parsing logic.
"""

import csv
import json
import sys
from io import StringIO


def validate_question_row(row, row_number):
    """
    Validate a single question row from CSV.
    
    Returns: (is_valid, error_message)
    """
    required_fields = ['question_text', 'answer_options', 'correct_answer']
    
    # Check required fields
    for field in required_fields:
        if field not in row or not row[field].strip():
            return False, f"Row {row_number}: Missing required field '{field}'"
    
    # Validate answer_options is valid JSON
    try:
        options = json.loads(row['answer_options'])
        if not isinstance(options, (list, dict)):
            return False, f"Row {row_number}: answer_options must be a JSON array or object"
        if isinstance(options, list) and len(options) < 2:
            return False, f"Row {row_number}: answer_options must have at least 2 options"
    except json.JSONDecodeError:
        return False, f"Row {row_number}: Invalid JSON in answer_options"
    
    # Validate correct_answer is not empty
    if not row['correct_answer'].strip():
        return False, f"Row {row_number}: correct_answer cannot be empty"
    
    # Validate difficulty if provided
    if row.get('difficulty'):
        valid_difficulties = ['easy', 'medium', 'hard', 'expert']
        if row['difficulty'].lower() not in valid_difficulties:
            return False, f"Row {row_number}: difficulty must be one of {valid_difficulties}"
    
    return True, None


def test_csv_file(filepath):
    """Test CSV file validation."""
    print(f"\n{'='*60}")
    print(f"Testing CSV file: {filepath}")
    print(f"{'='*60}\n")
    
    stats = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'errors': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate CSV has required columns
            required_columns = {'question_text', 'answer_options', 'correct_answer'}
            if not required_columns.issubset(set(reader.fieldnames)):
                missing = required_columns - set(reader.fieldnames)
                print(f"❌ CSV missing required columns: {missing}")
                return False
            
            print(f"✓ CSV has all required columns: {', '.join(required_columns)}")
            print(f"✓ Additional columns: {', '.join(set(reader.fieldnames) - required_columns)}\n")
            
            for idx, row in enumerate(reader, start=2):
                stats['total'] += 1
                
                is_valid, error_msg = validate_question_row(row, idx)
                if not is_valid:
                    stats['invalid'] += 1
                    stats['errors'].append(error_msg)
                    print(f"❌ {error_msg}")
                else:
                    stats['valid'] += 1
                    print(f"✓ Row {idx}: Valid - {row['question_text'][:50]}...")
        
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Total rows: {stats['total']}")
        print(f"Valid rows: {stats['valid']} ({stats['valid']/stats['total']*100:.1f}%)")
        print(f"Invalid rows: {stats['invalid']} ({stats['invalid']/stats['total']*100:.1f}%)")
        
        if stats['invalid'] > 0:
            print(f"\n❌ {stats['invalid']} validation errors found")
            return False
        else:
            print(f"\n✅ All rows are valid!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False


def main():
    """Run tests on sample CSV files."""
    print("\n" + "="*60)
    print("CSV Question Import - Validation Test")
    print("="*60)
    
    test_files = [
        'samples/sample_questions.csv',
        'samples/sample_questions_advanced.csv'
    ]
    
    all_passed = True
    
    for filepath in test_files:
        result = test_csv_file(filepath)
        all_passed = all_passed and result
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("="*60)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
