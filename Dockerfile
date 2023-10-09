FROM python:3.9-slim

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN pip install virtualenv && \
    virtualenv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
