# ------------------------------------------------------------
# FastAPI Cloud Run Dockerfile (확실히 uvicorn 실행되도록)
# ------------------------------------------------------------
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080
ENV PORT=8080

# 👇 핵심: ENTRYPOINT를 명시적으로 지정
ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
