"""
Aprendiz CSV Question Ingestion Service
Flask application for importing questions from CSV files into PostgreSQL database.
"""

from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import psycopg2
from psycopg2.extras import execute_values
import csv
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'aprendiz'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}


def get_db_connection():
    """Establish database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        raise


def init_database():
    """Initialize database schema if it doesn't exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                question_text TEXT NOT NULL,
                answer_options JSONB NOT NULL,
                correct_answer TEXT NOT NULL,
                category VARCHAR(100),
                difficulty VARCHAR(20),
                explanation TEXT,
                tags TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_questions_category 
            ON questions(category);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_questions_difficulty 
            ON questions(difficulty);
        """)
        
        # Create import_logs table for tracking imports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS import_logs (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                total_records INTEGER,
                successful_imports INTEGER,
                failed_imports INTEGER,
                error_details JSONB,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Database schema initialized successfully")
    except psycopg2.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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


def process_csv_file(filepath):
    """
    Process CSV file and import questions into database.
    
    Returns: dict with import statistics
    """
    stats = {
        'total': 0,
        'successful': 0,
        'failed': 0,
        'errors': []
    }
    
    questions_to_insert = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate CSV has required columns
            required_columns = {'question_text', 'answer_options', 'correct_answer'}
            if not required_columns.issubset(set(reader.fieldnames)):
                missing = required_columns - set(reader.fieldnames)
                raise ValueError(f"CSV missing required columns: {missing}")
            
            for idx, row in enumerate(reader, start=2):  # Start from 2 (header is 1)
                stats['total'] += 1
                
                # Validate row
                is_valid, error_msg = validate_question_row(row, idx)
                if not is_valid:
                    stats['failed'] += 1
                    stats['errors'].append(error_msg)
                    continue
                
                # Parse tags if present
                tags = []
                if row.get('tags'):
                    tags = [tag.strip() for tag in row['tags'].split(',')]
                
                # Prepare question data
                question_data = (
                    row['question_text'].strip(),
                    json.loads(row['answer_options']),
                    row['correct_answer'].strip(),
                    row.get('category', '').strip() or None,
                    row.get('difficulty', '').strip().lower() or None,
                    row.get('explanation', '').strip() or None,
                    tags if tags else None
                )
                
                questions_to_insert.append(question_data)
                stats['successful'] += 1
        
        # Bulk insert valid questions
        if questions_to_insert:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            execute_values(
                cursor,
                """
                INSERT INTO questions 
                (question_text, answer_options, correct_answer, category, 
                 difficulty, explanation, tags)
                VALUES %s
                """,
                questions_to_insert
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Successfully inserted {stats['successful']} questions")
    
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        stats['errors'].append(f"Processing error: {str(e)}")
        raise
    
    return stats


def log_import(filename, stats):
    """Log import statistics to database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO import_logs 
            (filename, total_records, successful_imports, failed_imports, error_details)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                filename,
                stats['total'],
                stats['successful'],
                stats['failed'],
                json.dumps(stats['errors']) if stats['errors'] else None
            )
        )
        
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        logger.error(f"Failed to log import: {e}")


@app.route('/')
def index():
    """Render main upload page."""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    
    try:
        # Save file securely
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        # Process CSV
        stats = process_csv_file(filepath)
        
        # Log import
        log_import(filename, stats)
        
        # Clean up uploaded file (optional - keep for audit trail)
        # os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': f'Import completed',
            'statistics': {
                'total_records': stats['total'],
                'successful_imports': stats['successful'],
                'failed_imports': stats['failed'],
                'errors': stats['errors'][:10]  # Limit errors in response
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': f'Import failed: {str(e)}'}), 500


@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Retrieve questions with optional filtering."""
    try:
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM questions WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if difficulty:
            query += " AND difficulty = %s"
            params.append(difficulty)
        
        query += " ORDER BY id DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        
        columns = [desc[0] for desc in cursor.description]
        questions = []
        
        for row in cursor.fetchall():
            question = dict(zip(columns, row))
            # Convert datetime to ISO format
            if question.get('created_at'):
                question['created_at'] = question['created_at'].isoformat()
            if question.get('updated_at'):
                question['updated_at'] = question['updated_at'].isoformat()
            questions.append(question)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'questions': questions,
            'count': len(questions),
            'limit': limit,
            'offset': offset
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving questions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total questions
        cursor.execute("SELECT COUNT(*) FROM questions")
        total_questions = cursor.fetchone()[0]
        
        # Questions by category
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM questions 
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
        """)
        by_category = [{'category': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Questions by difficulty
        cursor.execute("""
            SELECT difficulty, COUNT(*) as count 
            FROM questions 
            WHERE difficulty IS NOT NULL
            GROUP BY difficulty
            ORDER BY 
                CASE difficulty
                    WHEN 'easy' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'hard' THEN 3
                    WHEN 'expert' THEN 4
                END
        """)
        by_difficulty = [{'difficulty': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Recent imports
        cursor.execute("""
            SELECT filename, total_records, successful_imports, 
                   failed_imports, imported_at
            FROM import_logs
            ORDER BY imported_at DESC
            LIMIT 10
        """)
        recent_imports = []
        for row in cursor.fetchall():
            recent_imports.append({
                'filename': row[0],
                'total_records': row[1],
                'successful_imports': row[2],
                'failed_imports': row[3],
                'imported_at': row[4].isoformat()
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'total_questions': total_questions,
            'by_category': by_category,
            'by_difficulty': by_difficulty,
            'recent_imports': recent_imports
        }), 200
    
    except Exception as e:
        logger.error(f"Error retrieving stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/samples/<filename>')
def download_sample(filename):
    """Download sample CSV files."""
    return send_from_directory('/app/samples', filename)


if __name__ == '__main__':
    # Initialize database on startup
    try:
        init_database()
        logger.info("Application starting...")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        exit(1)
    
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
