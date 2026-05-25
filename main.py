from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4

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


tasks = []
categories = []


@app.get("/categories", status_code=status.HTTP_200_OK)
def get_categories():


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
    for key, value in payload.items():
        setattr(task, key, value)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    task = check_task_exists(task_id)
    tasks.remove(task)


# CATEGORIES #

@app.get('/categories', status_code=status.HTTP_200_OK)
def get_categories():
    return categories


