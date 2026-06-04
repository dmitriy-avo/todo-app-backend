from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)

    def create(self, category_name: str) -> CategoryORM:
        new_category = CategoryORM(name=category_name)
        self.db.add(new_category)
        return new_category

    def delete(self, category_for_delete: CategoryORM) -> None:
        self.db.delete(category_for_delete)
