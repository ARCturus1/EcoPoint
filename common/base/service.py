from typing import Any

from pydantic import BaseModel

from ..errors import DuplicateException, MissingException
from .schema import SqlAlchemyBase
from .data import BaseRepository

import logging


class BaseService[
    ResponseModel: BaseModel,
    CreateModel: BaseModel,
    UpdateModel: BaseModel,
    SchemaModel: SqlAlchemyBase,
]:
    schema_response: type[ResponseModel]
    schema_create: type[CreateModel]
    schema_update: type[UpdateModel]

    dataCrud: BaseRepository[SchemaModel, ResponseModel, CreateModel, UpdateModel]

    async def create(self, obj_in: CreateModel) -> ResponseModel | None:
        """
        Create a new record in the database.

        Args:
            obj_in: Pydantic schema instance containing the data to create.

        Returns:
            ResponseModel: The created record as a response schema, or None if creation fails.

        Raises:
            DuplicateException: If a record with the same data already exists.
            Exception: If the database operation fails.
        """
        try:
            result = await self.dataCrud.create(obj_in)

            if result is None:
                return None

            return result

        except DuplicateException as exc:
            # Re-raise duplicate exceptions with context
            raise DuplicateException(
                message=f"Failed to create record: {exc.message}"
            ) from exc

        except Exception as exc:
            # Log unexpected errors for debugging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Unexpected error during record creation: {str(exc)}", exc_info=True
            )

            # Re-raise with context
            raise Exception(f"Failed to create record: {str(exc)}") from exc

    # dataGet: BaseGetData[SchemaModel, ResponseModel] = BaseGetData[
    #     SchemaModel, ResponseModel
    # ]()

    async def get_all(self) -> list[ResponseModel]:
        """
        Retrieve all records from the database.

        This method fetches all records from the database and returns them as a list
        of response models. If no records are found or the database operation fails,
        an empty list is returned to maintain API contract consistency.

        Returns:
            list[ResponseModel]: A list of response models. Returns an empty list if
                no records are found or if an error occurs.

        Raises:
            DatabaseError: If the database operation fails unexpectedly.
            Exception: For any other unexpected errors during retrieval.

        Performance Considerations:
            - For large datasets, consider implementing pagination
            - Consider adding caching for frequently accessed data
            - Consider adding filtering and sorting options
        """
        try:
            result = await self.dataCrud.get_all()

            # Handle None case (no records found)
            if result is None:
                return []

            # Validate result is a list
            if not isinstance(result, list):
                raise TypeError(
                    f"Expected list of ResponseModel, got {type(result).__name__}"
                )

            # Validate all items are ResponseModel instances
            for item in result:
                if not isinstance(item, self.schema_response):
                    raise TypeError(
                        f"Expected ResponseModel instance, got {type(item).__name__}"
                    )

            return result

        except Exception as exc:
            # Log unexpected errors for debugging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Unexpected error during get_all operation: {str(exc)}", exc_info=True
            )

            # Re-raise with context for proper error handling
            raise Exception(f"Failed to retrieve all records: {str(exc)}") from exc

    async def get_one(self, **filter: Any) -> ResponseModel | None:
        """
        Retrieve a single record from the database based on the provided filters.

        This method fetches a single record matching the given filter criteria.
        If no record is found, returns None. The method includes comprehensive
        error handling and validation to ensure data integrity.

        Args:
            **filter: Keyword arguments representing the filter criteria for the query.
                     Common examples include id, user_id, or other unique identifiers.

        Returns:
            ResponseModel: The retrieved record as a response schema, or None if no
                          matching record is found.

        Raises:
            ValueError: If no filter criteria are provided.
            DatabaseError: If the database operation fails unexpectedly.
            Exception: For any other unexpected errors during retrieval.

        Performance Considerations:
            - For frequently accessed records, consider implementing caching
            - Ensure filter criteria are indexed in the database for optimal performance
            - Consider adding timeout handling for long-running queries

        Edge Cases Handled:
            - No filter criteria provided
            - Record not found in database
            - Database connection issues
            - Unexpected data types or structures
        """
        try:
            # Validate that filter criteria are provided
            if not filter:
                raise ValueError(
                    "Filter criteria must be provided to retrieve a record"
                )

            # Execute the database query
            result = await self.dataCrud.get_one(**filter)

            # Handle case where no record is found
            if result is None:
                return None

            # Validate result type
            if not isinstance(result, self.schema_response):
                raise TypeError(
                    f"Expected ResponseModel instance, got {type(result).__name__}"
                )

            return result

        except ValueError as exc:
            # Re-raise validation errors with context
            raise ValueError(f"Failed to retrieve record: {str(exc)}") from exc

        except Exception as exc:
            # Log unexpected errors for debugging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Unexpected error during get_one operation: {str(exc)}", exc_info=True
            )

            # Re-raise with context for proper error handling
            raise Exception(f"Failed to retrieve record: {str(exc)}") from exc

    # dataUpdate: BaseUpdateData[SchemaModel, ResponseModel, UpdateModel] = (
    #     BaseUpdateData[SchemaModel, ResponseModel, UpdateModel](dataGet)
    # )

    async def modify(self, obj_in: UpdateModel, **filters: Any) -> ResponseModel | None:
        """
        Update an existing record in the database.

        This method delegates the update operation to the underlying data CRUD layer.
        It includes comprehensive error handling, logging, and validation to ensure
        data integrity and provide meaningful feedback in case of failures.

        Args:
            obj_in: Pydantic schema instance containing the data to update.
            **filters: Keyword arguments to identify the record to update (e.g., id=1).

        Returns:
            ResponseModel: The updated record as a response schema, or None if no update occurred.

        Raises:
            MissingException: If no record matches the provided filters.
            DuplicateException: If a duplicate record would be created (if applicable).
            Exception: If the database operation fails unexpectedly.

        Performance Considerations:
            - The operation is transactional and will be committed automatically
            - Consider adding caching for frequently updated records
            - For large datasets, ensure filters are specific enough

        Best Practices:
            - Always provide specific filters to identify the record
            - Use Pydantic models for input validation
            - Handle None return value appropriately in calling code
        """
        try:
            # Validate that obj_in is not None
            if obj_in is None:
                raise ValueError("Update object cannot be None")

            # Call the underlying data CRUD layer
            result = await self.dataCrud.modify(obj_in=obj_in, **filters)

            # Handle None case (no update occurred)
            if result is None:
                return None

            # Validate result is a ResponseModel instance
            if not isinstance(result, self.schema_response):
                raise TypeError(
                    f"Expected ResponseModel instance, got {type(result).__name__}"
                )

            return result

        except MissingException as exc:
            # Re-raise missing exceptions with context
            raise MissingException(
                message=f"Failed to update record: {exc.message}"
            ) from exc

        except DuplicateException as exc:
            # Re-raise duplicate exceptions with context
            raise DuplicateException(
                message=f"Failed to update record: {exc.message}"
            ) from exc

        except Exception as exc:
            # Log unexpected errors for debugging
            logger = logging.getLogger(__name__)
            logger.error(
                f"Unexpected error during record update: {str(exc)}", exc_info=True
            )

            # Re-raise with context for proper error handling
            raise Exception(f"Failed to update record: {str(exc)}") from exc

    # dataDelete: BaseDeleteData[SchemaModel] = BaseDeleteData[SchemaModel]()

    async def delete(self, **filters: Any) -> bool:
        """
        Delete a record from the database based on the provided filters.

        Args:
            **filters: Keyword arguments to identify the record to delete.
                       Must include at least one filter condition.

        Returns:
            True if deletion was successful, False otherwise.

        Raises:
            ValueError: If no filters are provided.
            MissingException: If no record matches the filters.
            DatabaseError: If database operation fails.

        Example:
            >>> await service.delete(id=1)
            True
        """
        # Validate that filters are provided
        if not filters:
            raise ValueError("At least one filter must be provided for deletion")

        # Log the deletion attempt for audit purposes

        logger = logging.getLogger(__name__)
        logger.info(
            f"Attempting to delete record from {self.dataCrud.model.__tablename__} "
            f"with filters: {filters}"
        )

        try:
            # Execute the deletion operation
            result = await self.dataCrud.delete(**filters)

            # Log successful deletion
            logger.info(
                f"Successfully deleted record from {self.dataCrud.model.__tablename__} "
                f"with filters: {filters}"
            )

            return result

        except Exception as exc:
            # Log unexpected errors for debugging
            logger.error(
                f"Error deleting record from {self.dataCrud.model.__tablename__}: {str(exc)}",
                exc_info=True,
            )

            # Re-raise with context for proper error handling
            raise Exception(f"Failed to delete record: {str(exc)}") from exc
