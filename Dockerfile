FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl ffmpeg build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install setuptools wheel setuptools_scm --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py index.html ./
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
