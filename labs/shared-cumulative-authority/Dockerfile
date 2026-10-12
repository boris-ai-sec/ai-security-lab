FROM python:3.14-slim
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock
COPY lab lab
COPY tests tests
COPY grant.json .
USER 1000:1000
