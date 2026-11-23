FROM python:3.12-slim

WORKDIR /app

# Сначала зависимости — так Docker кэширует этот слой
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# timeout с запасом: при первом запуске датасет может скачиваться
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:create_app()"]
