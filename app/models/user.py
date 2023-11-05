# Third-Party --------------------------------------------------------------------------
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

# Project ------------------------------------------------------------------------------
from app.db.base_class import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User database model."""

    pass
