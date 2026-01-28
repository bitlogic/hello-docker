FROM python:3.11-slim

WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY fermat_verifier.py .
COPY README.md .

# Instalar dependencias (si las hay)
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el verificador
CMD ["python", "fermat_verifier.py"]
