## ./api-service/Dockerfile
## Using an official Python runtime as a parent image

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV NAME World

CMD ["python", "app.py"]


