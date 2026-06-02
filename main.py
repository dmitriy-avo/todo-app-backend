from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

from config import settings

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)

class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('starting lifespan')
    Base.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:3000"],
                   allow_methods=["*"],
                   )


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


class TaskSchema(BaseModel):
    id: str = Field(..., title="Task ID")
    title: str = Field(..., title="Task Title")
    completed: bool = Field(default=False, description="Whether the task has been completed")


class TaskCreateSchema(BaseModel):
    title: str = Field(..., title="Task Title")


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., title="Task Title")

class CategorySchema(CategoryCreateSchema):
    id: str = Field(..., title="Category ID")

class CategoryUpdateSchema(BaseModel):
    name: str | None = None


tasks = []
categories = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_category_exists(category_id: str):
    all_categories_ids = [c.id for c in categories]
    if category_id not in all_categories_ids:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories[all_categories_ids.index(category_id)]

def check_task_exists(task_id: str):
    all_messages_ids = [t.id for t in tasks]
    if task_id not in all_messages_ids:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[all_messages_ids.index(task_id)]

def task_to_model(task: TaskORM) -> TaskSchema:
    return TaskSchema(id=task.id, title=task.title, completed=task.completed)

def category_to_model(category: CategoryORM) -> CategorySchema:
    return CategorySchema(id=category.id, name=category.name)
# TaskReadSchema(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="Сделать ДЗ", completed=False)


@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)

    db.add(new_task)
    db.commit()
    return task_to_model(new_task)


@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(payload: TaskUpdateSchema, task_id: str, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()


# CATEGORIES #

@app.get('/categories', status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    all_categories = db.scalars(select(CategoryORM)).all()
    return [category_to_model(c) for c in all_categories]

@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_categorie(data: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name=data.name)
    db.add(new_category)
    db.commit()
    return category_to_model(new_category)


@app.patch('/categories/{category_id}', status_code=status.HTTP_200_OK)
def update_category(data: CategoryCreateSchema, category_id: str, db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoryORM, category_id)
    if data.name:
        category_for_update.name = data.name
    db.commit()
    return category_to_model(category_for_update)





@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    category_for_delete = db.get(CategoryORM, category_id)
    db.delete(category_for_delete)
    db.commit()





