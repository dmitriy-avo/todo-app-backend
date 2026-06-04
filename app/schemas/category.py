from pydantic import BaseModel, Field, ConfigDict


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., title="Category name")


class CategorySchema(CategoryCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., title="Category ID")


class CategoryUpdateSchema(BaseModel):
    name: str | None = None
