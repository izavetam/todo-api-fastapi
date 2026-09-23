from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Настройка базы данных
DATABASE_URL = 'sqlite:///./tasks.db'

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Модель базы данных
class TaskDB(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default='')
    deadline = Column(String, default='')
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    done = Column(Boolean, default=False)


# Создаем таблицу
Base.metadata.create_all(bind=engine)


# Pydantic-модели
class TaskCreate(BaseModel):
    title: str
    description: str = ''
    deadline: str = ''


class Task(TaskCreate):
    id: int
    created_at: str
    done: bool = False

    class Config:
        from_attributes = True


# Подключение к базе
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Приложение
app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "Привет! Это мой первый API"}


# Создание задачи
@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskDB(
        title=task.title,
        description=task.description,
        deadline=task.deadline
    )
    db.add(new_task)
    db.commit() 
    db.refresh(new_task) 
    return new_task


# Список всех задач
@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()


# Одна задача по ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return task


# Обновление задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    task.title = task_update.title
    task.description = task_update.description 
    task.deadline = task_update.deadline
    db.commit()
    db.refresh(task)
    return task


# Удаление задачи
@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    db.delete(task)
    db.commit()
    return {'message': f"Задача {task_id} удалена"} 