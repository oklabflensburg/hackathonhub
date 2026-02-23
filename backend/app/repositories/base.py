"""
Base repository class providing common CRUD operations.
"""
from typing import TypeVar, Type, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.domain.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record."""
        # Filter out fields that don't exist in the model
        model_fields = {column.name for column in self.model.__table__.columns}
        filtered_data = {k: v for k, v in obj_in.items() if k in model_fields}
        db_obj = self.model(**filtered_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]
    ) -> ModelType:
        """Update an existing record."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> bool:
        """Delete a record by ID."""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

    def count(self, db: Session) -> int:
        """Count total records."""
        return db.query(self.model).count()

    def exists(self, db: Session, id: int) -> bool:
        """Check if a record exists by ID."""
        return db.query(self.model).filter(self.model.id == id).first() is not None

    def filter(
        self, db: Session, *, skip: int = 0, limit: int = 100, **filters
    ) -> List[ModelType]:
        """Filter records by given criteria."""
        query = db.query(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                if value is None:
                    query = query.filter(getattr(self.model, field).is_(None))
                else:
                    query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()

    def order_by(
        self, db: Session, *, order_field: str, descending: bool = False,
        skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get records ordered by a field."""
        if not hasattr(self.model, order_field):
            raise AttributeError(f"Model has no attribute '{order_field}'")

        field = getattr(self.model, order_field)
        if descending:
            field = desc(field)
        else:
            field = asc(field)

        return db.query(self.model).order_by(field).offset(skip).limit(limit).all()
