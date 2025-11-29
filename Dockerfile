# ============================================
# Dockerfile для Flask приложения
# ============================================

# Базовый образ - официальный Python
# alpine - минималистичный Linux, меньше размер образа
FROM python:3.11-slim

# Метаданные образа
LABEL maintainer="SpecopsRF"
LABEL description="Task Manager Flask Application"
LABEL version="1.0"

# Устанавливаем переменные окружения
# PYTHONDONTWRITEBYTECODE - не создавать .pyc файлы
# PYTHONUNBUFFERED - не буферизировать вывод (важно для логов)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаём рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
# Нужны для psycopg2 (драйвер PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей отдельно
# Это позволяет использовать кэш Docker при изменении кода
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app/ ./app/

# Создаём непривилегированного пользователя для безопасности
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Указываем порт, который слушает приложение
EXPOSE 5000

# Команда запуска
# gunicorn - production-ready WSGI сервер
# -b 0.0.0.0:5000 - слушаем на всех интерфейсах
# -w 2 - количество воркеров
# app.main:app - путь к Flask приложению
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app.main:app"]
