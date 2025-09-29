FROM python:3.10-slim
WORKDIR /home/ubuntu/Desktop/ipa2025-msapp/scheduler
COPY requirements.txt .
COPY  ./producer.py .
COPY  ./scheduler.py .
COPY  ./database.py .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
CMD python scheduler.py
