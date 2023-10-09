FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate

EXPOSE 8000

ENV NAME World

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
