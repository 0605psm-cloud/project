# ------------------------------------------------------------
# FastAPI Cloud Run Dockerfile (권장 안정 버전)
# ------------------------------------------------------------
FROM python:3.11-slim

# 1. 작업 디렉토리
WORKDIR /app

# 2. 종속성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 소스 복사
COPY . .

# 4. Cloud Run 기본 포트
EXPOSE 8080

# 5. ENTRYPOINT를 명시적으로 uvicorn으로 설정
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
