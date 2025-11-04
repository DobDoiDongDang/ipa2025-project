FROM python:3.10-slim
WORKDIR /ipa2025-project/scheduler
COPY requirements.txt .
COPY  ./producer.py .
COPY  ./scheduler.py .
COPY  ./database.py .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
CMD python -u scheduler.py
