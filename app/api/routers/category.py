from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_category_service
from app.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from app.services.category import CategoryService


category_router = APIRouter(prefix="/categories", tags=["categories"])



@category_router.get('', status_code=status.HTTP_200_OK)
def read_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategorySchema]:
    return category_service.list_category()


@category_router.post('', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema,
                     category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    return category_service.create_category(payload)


@category_router.patch('/{category_id}', status_code=status.HTTP_200_OK)
def update_category(payload: CategoryUpdateSchema, category_id: str,
                    category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    return category_service.update_category(category_id=category_id, category_update=payload)


@category_router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service: CategoryService = Depends(get_category_service)) -> None:
    return category_service.delete_category(category_id=category_id)
