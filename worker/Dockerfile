FROM python:3.10-slim
WORKDIR /ipa2025-project/worker
COPY requirements.txt .
COPY  ./worker.py .
COPY  ./get_router_data.py .
COPY ./get_data.py .
COPY ./config_loopback.py .
COPY ./config_router_interface.py .
COPY  ./save_data.py .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
CMD echo "HELLOOOO"
CMD python -u worker.py
