from pydantic import BaseModel, Field, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., title="Task ID")
    title: str = Field(..., title="Task Title")
    completed: bool = Field(default=False, description="Whether the task has been completed")


class TaskCreateSchema(BaseModel):
    title: str = Field(..., title="Task Title")


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
