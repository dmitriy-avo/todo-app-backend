from fastapi import FastAPI
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


tasks = []


# TaskReadSchema(id="3fa85f64-5717-4562-b3fc-2c963f66afa6", title="Сделать ДЗ", completed=False)


@app.get("/tasks")
async def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks")
async def create_task(payload: TaskCreateSchema) -> TaskSchema:
    global tasks
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task
