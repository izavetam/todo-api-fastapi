# To-Do API

REST API для управления задачами на FastAPI с базой данных SQLite.

## Что умеет
- Создание задачи (POST /tasks)
- Просмотр всех задач (GET /tasks)
- Просмотр одной задачи (GET /tasks/{id})
- Обновление задачи (PUT /tasks/{id})
- Удаление задачи (DELETE /tasks/{id})
- Валидация данных (Pydantic)
- Обработка ошибок (404)

## Технологии
- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Установка
```bash
pip install fastapi uvicorn sqlalchemy

## Запуск
uvicorn main:app --reload

## Документация
После запуска: http://127.0.0.1:8000/docs

## Автор
izavetam — студентка 2 курса ИБ
GitHub: @izavetam
