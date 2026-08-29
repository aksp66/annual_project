# API FastAPI de génération DDPM/GAN (cf. app/api/main.py, docker-compose.yml)
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY configs/ configs/
COPY app/api/ app/api/

# Checkpoints montés en volume (docker-compose.yml) — trop volumineux/non
# versionnés pour être copiés dans l'image, cf. .gitignore.
EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
