# Dockerfile
FROM python:3

WORKDIR /src

COPY . /src

CMD ["python3", "app.py"]
