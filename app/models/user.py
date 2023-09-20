from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
