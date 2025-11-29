# 📝 Task Manager - DevOps Demo Project

[![CI/CD Pipeline](https://github.com/SpecopsRF/repos_2/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/SpecopsRF/repos_2/actions/workflows/ci-cd.yml)

Простое веб-приложение для управления задачами, демонстрирующее DevOps практики.

## 🚀 Возможности

- ✅ Создание, редактирование и удаление задач
- ✅ Docker контейнеризация
- ✅ CI/CD с GitHub Actions
- ✅ Автоматическое тестирование
- ✅ SAST сканирование (Bandit)
- ✅ DAST сканирование (OWASP ZAP)

## 🛠 Технологии

- **Backend:** Python 3.11, Flask
- **Database:** PostgreSQL 15
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Security:** Bandit (SAST), OWASP ZAP (DAST)

## 📦 Быстрый старт

### Требования
- Docker и Docker Compose
- Git

### Запуск

```bash
# Клонируем репозиторий
git clone https://github.com/SpecopsRF/repos_2.git
cd repos_2

# Копируем файл окружения
cp .env.example .env

# Запускаем
docker compose up -d

# Открываем в браузере
# http://localhost:5000
Остановка

Bash
docker compose down
🧪 Тестирование

Bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
pytest tests/ -v

# С покрытием
pytest tests/ --cov=app --cov-report=html
🔒 Безопасность
SAST (Bandit)

Bash
pip install bandit
bandit -r app/ -ll
DAST (OWASP ZAP)
Выполняется автоматически в CI/CD пайплайне.

📁 Структура проекта

Nix
repos_2/
├── app/                    # Код приложения
│   ├── main.py            # Flask приложение
│   ├── templates/         # HTML шаблоны
│   └── static/            # CSS, JS
├── tests/                  # Тесты
├── .github/workflows/      # CI/CD пайплайны
├── Dockerfile             # Docker образ приложения
├── Dockerfile.db          # Docker образ БД
├── docker-compose.yml     # Оркестрация контейнеров
└── requirements.txt       # Python зависимости
🌐 API Endpoints
Метод	Путь	Описание
GET	/	Главная страница
GET	/tasks	Список задач
POST	/tasks/add	Добавить задачу
POST	/tasks/<id>/toggle	Переключить статус
POST	/tasks/<id>/delete	Удалить задачу
GET	/api/health	Health check
GET	/api/tasks	API: список задач
POST	/api/tasks	API: создать задачу
📝 Лицензия
MIT License
