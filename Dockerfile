FROM python:3.11-alpine

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
