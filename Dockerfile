FROM python:3.12.8-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py migrate && daphne -b 0.0.0.0 -p 8000 restaurantsystem.asgi:application
