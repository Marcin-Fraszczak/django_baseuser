FROM python:3.11.4-alpine3.18

WORKDIR /app
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT python manage.py runserver 0.0.0.0:8000