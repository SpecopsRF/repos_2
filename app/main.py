"""
Главный файл Flask приложения - простой Task Manager
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Создаём экземпляр Flask приложения
app = Flask(__name__)

# Конфигурация приложения
# SECRET_KEY нужен для сессий и flash-сообщений
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Строка подключения к PostgreSQL
# Формат: postgresql://пользователь:пароль@хост:порт/имя_базы
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://taskuser:taskpassword@db:5432/taskdb'
)

# Отключаем отслеживание изменений (экономит память)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем SQLAlchemy
db = SQLAlchemy(app)


# Модель задачи (таблица в БД)
class Task(db.Model):
    """
    Модель задачи для хранения в базе данных
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }


# Создаём таблицы при первом запуске
with app.app_context():
    db.create_all()


# === МАРШРУТЫ (ROUTES) ===

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/tasks')
def tasks_list():
    """Страница со списком задач"""
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/tasks/add', methods=['POST'])
def add_task():
    """Добавление новой задачи"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    
    if not title:
        flash('Название задачи обязательно!', 'error')
        return redirect(url_for('tasks_list'))
    
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    
    flash('Задача успешно добавлена!', 'success')
    return redirect(url_for('tasks_list'))


@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """Переключение статуса задачи (выполнена/не выполнена)"""
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    
    status = 'выполнена' if task.completed else 'не выполнена'
    flash(f'Задача отмечена как {status}', 'success')
    return redirect(url_for('tasks_list'))


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Удаление задачи"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    flash('Задача удалена', 'success')
    return redirect(url_for('tasks_list'))


# === API ENDPOINTS (для тестирования) ===

@app.route('/api/health')
def health_check():
    """Проверка здоровья приложения"""
    return jsonify({'status': 'healthy', 'message': 'Application is running'})


@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    """API: получить все задачи"""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    """API: создать задачу"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', '')
    )
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201


# Запуск приложения
if __name__ == '__main__':
    # debug=True только для разработки!
    app.run(host='0.0.0.0', port=5000, debug=True)
