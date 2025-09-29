FROM python:3.10-slim
WORKDIR /home/ubuntu/Desktop/ipa2025-msapp/worker
COPY requirements.txt .
COPY  ./worker.py .
COPY  ./ssh_router.py .
COPY  ./save_data.py .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
CMD echo "HELLOOOO"
CMD python worker.py
