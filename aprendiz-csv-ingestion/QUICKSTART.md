# Quick Start Guide - Aprendiz CSV Question Ingestion

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Application
```bash
cd aprendiz-csv-ingestion
docker-compose up --build
```

Wait for the message: `Running on http://0.0.0.0:5000`

### Step 2: Open the Web Interface
Open your browser:
```
http://localhost:5000
```

### Step 3: Upload a CSV File
1. Download a sample CSV from the interface, or
2. Drag and drop your own CSV file
3. Click "Importar Preguntas"
4. View the results!

---

## 📁 CSV Format Example

Your CSV must have these columns:

```csv
question_text,answer_options,correct_answer,category,difficulty,explanation,tags
¿Cuál es la capital de Francia?,"[""París"", ""Londres"", ""Madrid""]",París,Geografía,easy,París es la capital de Francia.,"europa,capitales"
```

**Required:**
- `question_text`: The question
- `answer_options`: JSON array of options
- `correct_answer`: The correct answer

**Optional:**
- `category`: Question category
- `difficulty`: easy, medium, hard, or expert
- `explanation`: Why the answer is correct
- `tags`: Comma-separated tags

---

## 🔍 Verify It's Working

### Check Health
```bash
curl http://localhost:5000/health
```

Should return:
```json
{"status": "healthy", "database": "connected"}
```

### Upload Sample CSV
```bash
curl -X POST -F "file=@samples/sample_questions.csv" \
  http://localhost:5000/api/upload
```

### View Statistics
```bash
curl http://localhost:5000/api/stats
```

---

## 🛑 Stop the Application

```bash
docker-compose down
```

To also remove data:
```bash
docker-compose down -v
```

---

## ❓ Troubleshooting

**Port 5000 already in use?**
Edit `docker-compose.yml` and change `"5000:5000"` to `"5001:5000"`, then use `http://localhost:5001`

**Database connection error?**
Wait 10 seconds after startup for PostgreSQL to initialize

**CSV upload fails?**
- Check file is less than 16MB
- Verify file extension is `.csv`
- Validate JSON in `answer_options` column
- Ensure required columns exist

---

## 📊 What Happens When You Upload?

1. File is validated (size, type, format)
2. Each row is checked for required fields
3. JSON syntax is validated
4. Valid rows are inserted into PostgreSQL
5. Statistics are updated
6. Import is logged with success/error details

---

## 🎯 Next Steps

- View questions: `GET /api/questions`
- Filter by category: `GET /api/questions?category=Geografía`
- Filter by difficulty: `GET /api/questions?difficulty=easy`
- Check import history in the web interface

---

**Need Help?** See `README.md` for full documentation
