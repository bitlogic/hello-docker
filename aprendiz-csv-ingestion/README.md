# Aprendiz - CSV Question Ingestion System

A robust Flask-based application for importing educational questions from CSV files into a PostgreSQL database. Built with Docker for easy deployment and scalability.

## 🎯 Features

- **CSV Upload Interface**: Modern, user-friendly web interface for uploading CSV files
- **Bulk Import**: Efficiently process and import large question datasets
- **Data Validation**: Comprehensive validation of CSV data before import
- **Error Reporting**: Detailed error messages for failed imports
- **Statistics Dashboard**: Real-time statistics and import history
- **PostgreSQL Storage**: Reliable data persistence with indexed queries
- **Docker Support**: Complete containerized setup with Docker Compose
- **Health Checks**: Built-in health monitoring endpoints

## 🏗️ Architecture

```
aprendiz-csv-ingestion/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # Web interface
├── samples/                # Sample CSV files
│   ├── sample_questions.csv
│   └── sample_questions_advanced.csv
├── uploads/                # Uploaded files storage
├── Dockerfile              # Application container
├── docker-compose.yml      # Multi-container setup
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 📋 Prerequisites

- Docker 24.0 or later
- Docker Compose 2.0 or later

## 🚀 Quick Start

### 1. Build and Start Services

```bash
cd aprendiz-csv-ingestion
docker-compose up --build
```

### 2. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### 3. Upload CSV Files

- Use the web interface to drag and drop or select CSV files
- Download sample CSV files from the interface
- View import statistics and history

## 📊 CSV Format

The CSV file must contain the following columns:

| Column           | Required | Type   | Description                                    | Example                                      |
|------------------|----------|--------|------------------------------------------------|----------------------------------------------|
| `question_text`  | ✅ Yes   | String | The question text                              | ¿Cuál es la capital de Francia?              |
| `answer_options` | ✅ Yes   | JSON   | Answer options as JSON array or object         | ["París", "Londres", "Madrid", "Roma"]       |
| `correct_answer` | ✅ Yes   | String | The correct answer                             | París                                        |
| `category`       | ❌ No    | String | Question category                              | Geografía                                    |
| `difficulty`     | ❌ No    | String | Difficulty level (easy, medium, hard, expert)  | easy                                         |
| `explanation`    | ❌ No    | String | Explanation of the answer                      | París es la capital de Francia desde 987.    |
| `tags`           | ❌ No    | String | Comma-separated tags                           | europa, capitales, geografía                 |

### Sample CSV Row

```csv
question_text,answer_options,correct_answer,category,difficulty,explanation,tags
¿Cuál es la capital de Francia?,"[""París"", ""Londres"", ""Madrid"", ""Roma""]",París,Geografía,easy,París es la capital de Francia desde 987.,"europa,capitales,geografía"
```

## 🔌 API Endpoints

### Upload CSV
```http
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "message": "Import completed",
  "statistics": {
    "total_records": 10,
    "successful_imports": 9,
    "failed_imports": 1,
    "errors": ["Row 5: Invalid JSON in answer_options"]
  }
}
```

### Get Questions
```http
GET /api/questions?category=Geografía&difficulty=easy&limit=10&offset=0

Response:
{
  "questions": [...],
  "count": 10,
  "limit": 10,
  "offset": 0
}
```

### Get Statistics
```http
GET /api/stats

Response:
{
  "total_questions": 100,
  "by_category": [...],
  "by_difficulty": [...],
  "recent_imports": [...]
}
```

### Health Check
```http
GET /health

Response:
{
  "status": "healthy",
  "database": "connected"
}
```

## 🗄️ Database Schema

### Questions Table
```sql
CREATE TABLE questions (
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
```

### Import Logs Table
```sql
CREATE TABLE import_logs (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    total_records INTEGER,
    successful_imports INTEGER,
    failed_imports INTEGER,
    error_details JSONB,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

Environment variables can be configured in `docker-compose.yml`:

```yaml
environment:
  DB_HOST: postgres
  DB_PORT: 5432
  DB_NAME: aprendiz
  DB_USER: postgres
  DB_PASSWORD: password
  FLASK_DEBUG: "False"
```

## 📝 Development

### Local Development (without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL and configure environment variables:
```bash
export DB_HOST=localhost
export DB_NAME=aprendiz
export DB_USER=postgres
export DB_PASSWORD=password
```

3. Run the application:
```bash
python app.py
```

### Running Tests

```bash
# Test CSV upload
curl -X POST -F "file=@samples/sample_questions.csv" http://localhost:5000/api/upload

# Test health endpoint
curl http://localhost:5000/health

# Get statistics
curl http://localhost:5000/api/stats
```

## 🔍 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
docker-compose logs aprendiz-app

# Restart services
docker-compose restart
```

### Import Errors
- Verify CSV format matches the required schema
- Check for valid JSON in `answer_options` column
- Ensure required fields are not empty
- Review error details in the UI or API response

## 📦 Production Deployment

For production use:

1. **Change default passwords** in `docker-compose.yml`
2. **Use environment files** for sensitive configuration
3. **Set up volume backups** for PostgreSQL data
4. **Configure reverse proxy** (nginx/Apache) for HTTPS
5. **Set resource limits** in Docker Compose
6. **Enable monitoring** and logging

Example production configuration:
```yaml
services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Aprendiz Product 2026 initiative.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review application logs: `docker-compose logs`
- Open an issue in the project repository

## 🎓 Related

This application is part of the Aprendiz learning platform and demonstrates:
- Docker containerization
- PostgreSQL database design
- RESTful API development
- CSV data processing
- Modern web UI/UX

---

**Built with ❤️ for the Aprendiz Product 2026**
