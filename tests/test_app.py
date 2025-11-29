"""
Тесты для Flask приложения Task Manager

Запуск тестов:
    pytest tests/test_app.py -v

Запуск с покрытием:
    pytest tests/test_app.py --cov=app --cov-report=html
"""
import os
import sys
import pytest

# Добавляем корневую папку проекта в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Устанавливаем тестовую конфигурацию ДО импорта приложения
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # Используем SQLite для тестов
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['TESTING'] = '1'

from app.main import app, db, Task


@pytest.fixture
def client():
    """
    Фикстура создаёт тестовый клиент Flask
    Фикстура - это функция, которая подготавливает данные для теста
    """
    # Конфигурируем приложение для тестирования
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Создаём контекст приложения и таблицы
    with app.app_context():
        db.create_all()
        yield app.test_client()  # Возвращаем тестовый клиент
        db.drop_all()  # Очищаем после тестов


@pytest.fixture
def sample_task(client):
    """Фикстура создаёт тестовую задачу"""
    with app.app_context():
        task = Task(title='Тестовая задача', description='Описание')
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    return task_id


# ============================================
# Тесты главной страницы
# ============================================

class TestIndexPage:
    """Тесты для главной страницы"""
    
    def test_index_page_loads(self, client):
        """Тест: главная страница загружается"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_page_content(self, client):
        """Тест: главная страница содержит нужный текст"""
        response = client.get('/')
        assert b'Task Manager' in response.data
        assert b'Docker' in response.data


# ============================================
# Тесты страницы задач
# ============================================

class TestTasksPage:
    """Тесты для страницы задач"""
    
    def test_tasks_page_loads(self, client):
        """Тест: страница задач загружается"""
        response = client.get('/tasks')
        assert response.status_code == 200
    
    def test_tasks_page_empty(self, client):
        """Тест: пустой список задач"""
        response = client.get('/tasks')
        assert b'Задач пока нет' in response.data or response.status_code == 200


# ============================================
# Тесты добавления задач
# ============================================

class TestAddTask:
    """Тесты добавления задач"""
    
    def test_add_task_success(self, client):
        """Тест: успешное добавление задачи"""
        response = client.post('/tasks/add', data={
            'title': 'Новая задача',
            'description': 'Описание задачи'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Проверяем что редирект произошёл
        assert b'Новая задача' in response.data or b'успешно' in response.data
    
    def test_add_task_empty_title(self, client):
        """Тест: пустое название задачи"""
        response = client.post('/tasks/add', data={
            'title': '',
            'description': 'Описание'
        }, follow_redirects=True)
        
        assert response.status_code == 200


# ============================================
# Тесты API endpoints
# ============================================

class TestAPI:
    """Тесты для API"""
    
    def test_health_check(self, client):
        """Тест: проверка здоровья приложения"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_api_get_tasks(self, client):
        """Тест: получение списка задач через API"""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_api_create_task(self, client):
        """Тест: создание задачи через API"""
        response = client.post('/api/tasks', 
            json={'title': 'API Task', 'description': 'Created via API'},
            content_type='application/json'
        )
        
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['title'] == 'API Task'
    
    def test_api_create_task_no_title(self, client):
        """Тест: создание задачи без названия (ошибка)"""
        response = client.post('/api/tasks',
            json={'description': 'No title'},
            content_type='application/json'
        )
        
        assert response.status_code == 400


# ============================================
# Тесты операций с задачами
# ============================================

class TestTaskOperations:
    """Тесты операций с задачами"""
    
    def test_toggle_task(self, client, sample_task):
        """Тест: переключение статуса задачи"""
        response = client.post(f'/tasks/{sample_task}/toggle', follow_redirects=True)
        assert response.status_code == 200
    
    def test_delete_task(self, client, sample_task):
        """Тест: удаление задачи"""
        response = client.post(f'/tasks/{sample_task}/delete', follow_redirects=True)
        assert response.status_code == 200
    
    def test_toggle_nonexistent_task(self, client):
        """Тест: переключение несуществующей задачи"""
        response = client.post('/tasks/99999/toggle')
        assert response.status_code == 404
    
    def test_delete_nonexistent_task(self, client):
        """Тест: удаление несуществующей задачи"""
        response = client.post('/tasks/99999/delete')
        assert response.status_code == 404


# ============================================
# Тесты модели Task
# ============================================

class TestTaskModel:
    """Тесты для модели Task"""
    
    def test_task_creation(self, client):
        """Тест: создание объекта Task"""
        with app.app_context():
            task = Task(title='Test', description='Test Description')
            db.session.add(task)
            db.session.commit()
            
            assert task.id is not None
            assert task.title == 'Test'
            assert task.completed == False
    
    def test_task_to_dict(self, client):
        """Тест: преобразование Task в словарь"""
        with app.app_context():
            task = Task(title='Test', description='Desc')
            db.session.add(task)
            db.session.commit()
            
            task_dict = task.to_dict()
            assert 'id' in task_dict
            assert task_dict['title'] == 'Test'
            assert task_dict['completed'] == False


# ============================================
# Запуск тестов напрямую
# ============================================
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
