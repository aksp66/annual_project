# App Streamlit de démonstration DDPM vs GAN (cf. app/web/app.py, docker-compose.yml)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/web/ app/web/

EXPOSE 8501

CMD ["streamlit", "run", "app/web/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
