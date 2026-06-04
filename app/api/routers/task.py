from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_task_service
from app.schemas.task import TaskUpdateSchema, TaskCreateSchema, TaskSchema
from app.services.task import TaskService

task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.get("/", status_code=status.HTTP_200_OK)
def read_task(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()


@task_router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema,
                task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.create_task(task_create=payload)


@task_router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task(
        payload: TaskUpdateSchema,
        task_id: str,
        task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.update_task(task_id=task_id, task_update=payload)


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    return task_service.delete_task(task_id=task_id)


