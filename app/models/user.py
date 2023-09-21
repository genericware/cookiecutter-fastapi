from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from app.db.base_class import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """todo"""

    pass
