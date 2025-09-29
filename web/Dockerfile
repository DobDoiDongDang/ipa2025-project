FROM python:3.10-slim
WORKDIR /home/ubuntu/Desktop/ipa2025-msapp/web
COPY requirements.txt .
COPY  ./static ./static/
COPY  ./templates ./templates/
COPY  ./app.py .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
EXPOSE 8080
CMD python app.py

