-- Скрипт инициализации базы данных
-- Выполняется автоматически при первом запуске контейнера

-- Создаём таблицу задач (если не существует)
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Добавляем тестовые данные
INSERT INTO tasks (title, description, completed) VALUES 
    ('Изучить Docker', 'Разобраться с Dockerfile и docker-compose', true),
    ('Настроить CI/CD', 'Создать GitHub Actions пайплайн', false),
    ('Добавить тесты', 'Написать unit и integration тесты', false),
    ('Проверить безопасность', 'Запустить SAST и DAST сканеры', false);

-- Выводим сообщение
\echo 'Database initialized successfully!'
