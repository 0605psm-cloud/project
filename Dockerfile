# ------------------------------------------------------------
# FastAPI Cloud Run Dockerfile
# ------------------------------------------------------------
FROM python:3.11-slim

# 1. 작업 디렉터리 설정
WORKDIR /app

# 2. 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 소스 복사
COPY . .

# 4. 포트 개방
EXPOSE 8080

# 5. Cloud Run은 반드시 8080 포트를 LISTEN해야 함
ENV PORT=8080

# 6. FastAPI 앱 실행 (main.py 내부의 app을 지정)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
