"""
Base CRUD data class for FastAPI applications using SQLAlchemy and Pydantic.

This class provides a reusable foundation for implementing CRUD operations
with automatic schema validation, error handling, and database session management.
"""

from typing import Any, Optional
import logging

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from ..directives import SessionBase, connection

from ..errors import DuplicateException, MissingException
from .schema import SqlAlchemyBase


class BaseRepository[
    ModelType: SqlAlchemyBase,
    ResponseSchema: BaseModel,
    CreateSchema: BaseModel,
    UpdateSchema: BaseModel,
](SessionBase):
    """
    Generic base class for CRUD operations.

    Args:
        scheme: SQLAlchemy model class for database operations
        model_response: Pydantic schema for response serialization
        model_create: Pydantic schema for create operations
        model_update: Pydantic schema for update operations

    Example:
        >>> class User(Base):
        ...     __tablename__ = "users"
        ...     id = Column(Integer, primary_key=True)
        ...
        >>> class UserResponse(BaseModel):
        ...     id: int
        ...     name: str
        ...
        >>> class UserCreate(BaseModel):
        ...     name: str
        ...
        >>> class UserUpdate(BaseModel):
        ...     name: Optional[str] = None
        ...
        >>> class UserData(BaseCrudData[User, UserResponse, UserCreate, UserUpdate]):
        ...     scheme = User
        ...     model_response = UserResponse
        ...     model_create = UserCreate
        ...     model_update = UserUpdate
    """

    model: type[ModelType]
    schema_response: type[ResponseSchema]
    schema_create: type[CreateSchema]
    schema_update: type[UpdateSchema]

    def __init__(self, async_alchemy_session, **kwargs: Any) -> None:
        """Initialize the BaseCrudData instance."""
        self.async_alchemy_session = async_alchemy_session
        super().__init__(**kwargs)

    @connection()
    async def get_all(self) -> Optional[list[ResponseSchema]]:
        """
        Retrieve all records from the database.

        Returns:
            List of response schemas or None if no records found.

        Raises:
            DatabaseError: If database operation fails.
        """
        stmt = select(self.model)
        result = await self._session.execute(stmt)

        return [
            self.schema_response.model_validate(row, from_attributes=True)
            for row in result.scalars().all()
        ]

    @connection()
    async def get_one(self, **filters: Any) -> Optional[ResponseSchema]:
        """
        Retrieve a single record by filters.

        Args:
            **filters: Keyword arguments to filter the query.

        Returns:
            Response schema or None if not found.

        Raises:
            MissingException: If no record matches the filters.
            DatabaseError: If database operation fails.
        """
        stmt = select(self.model).filter_by(**filters)
        result = (await self._session.execute(stmt)).scalar_one_or_none()

        if not result:
            raise MissingException(
                message=f"{self.model.__tablename__} not found with filters: {filters}"
            )

        return self.schema_response.model_validate(result, from_attributes=True)

    @connection()
    async def create(self, obj_in: CreateSchema) -> Optional[ResponseSchema]:
        """
        Create a new record in the database.

        Args:
            obj_in: Pydantic schema instance with data to create.

        Returns:
            Response schema for the created record.

        Raises:
            DuplicateException: If a record with the same data already exists.
            DatabaseError: If database operation fails.
        """
        try:
            obj_out = self.model(**vars(obj_in))
            self._session.add(obj_out)
            await self._session.commit()
            await self._session.refresh(obj_out)

        except IntegrityError as exc:  # fix error handling
            print(exc)
            raise DuplicateException(
                message=f"Record with data {repr(obj_in)} already exists"
            ) from exc

        return self.schema_response.model_validate(obj_out, from_attributes=True)

    @connection(commit=True)
    async def modify(
        self, obj_in: UpdateSchema, **filters: Any
    ) -> Optional[ResponseSchema]:
        """
        Update an existing record in the database.

        Args:
            obj_in: Pydantic schema instance with data to update.
            **filters: Keyword arguments to identify the record to update.

        Returns:
            Response schema for the updated record, or None if no update occurred.

        Raises:
            MissingException: If no record matches the filters.
            DatabaseError: If database operation fails.
        """
        update_dict = self._filter_from_none_values(obj_in)

        if not update_dict:
            return None

        stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(**update_dict)
            .returning(self.model)
        )
        result = await self._session.execute(stmt)

        updated_obj = result.scalar_one_or_none()
        if not updated_obj:
            raise MissingException(
                message=f"{self.model.__tablename__} not found with filters: {filters}"
            )

        return self.schema_response.model_validate(updated_obj, from_attributes=True)

    @connection(commit=True)
    async def delete(self, **filters: Any) -> bool:
        """
        Delete a record from the database.

        Args:
            **filters: Keyword arguments to identify the record to delete.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            MissingException: If no record matches the filters.
            DatabaseError: If database operation fails.
        """
        stmt = delete(self.model).filter_by(**filters)
        result = await self._session.execute(stmt)

        if not result:
            raise MissingException(
                message=f"{self.model.__tablename__} not found with filters: {filters}"
            )

        return bool(result)

    def _filter_from_none_values(self, obj_in: UpdateSchema) -> dict[str, Any]:
        """
        Filter out None values from the update object.

        Args:
            obj_in: Pydantic schema instance to filter.

        Returns:
            Dictionary of non-None values.
        """
        return {key: value for key, value in vars(obj_in).items() if value is not None}

    # def __to_dict(self, obj: SchemeType):
    #     """Convert ORM object to dictionary."""
    #     return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    # def _to_response(self, obj: SchemeType) -> ResponseSchema:
    #     """Convert ORM object to Pydantic response schema."""
    #     return self.model_response.model_validate(obj)
