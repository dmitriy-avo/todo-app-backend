from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

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


app = FastAPI()
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


# TaskReadSchema(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="Сделать ДЗ", completed=False)


@app.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    global tasks
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(payload: TaskUpdateSchema, task_id: str) -> TaskSchema:
    task = check_task_exists(task_id)
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(task, key, value)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    task = check_task_exists(task_id)
    tasks.remove(task)


# CATEGORIES #

@app.get('/categories', status_code=status.HTTP_200_OK)
def get_categories() -> list[CategorySchema]:
    return categories

@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_categorie(data: CategoryCreateSchema) -> CategorySchema:
    global categories
    new_category = CategorySchema(
        id=str(uuid4()),
        name=data.name,
    )
    categories.append(new_category)
    return new_category

@app.patch('/categories/{category_id}', status_code=status.HTTP_200_OK)
def update_category(data: CategoryCreateSchema, category_id: str) -> CategorySchema:
    category = check_category_exists(category_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(category, key, value)
    return category

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str) -> None:
    category = check_category_exists(category_id)
    categories.remove(category)




