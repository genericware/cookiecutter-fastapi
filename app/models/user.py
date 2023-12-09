from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    """OAuth account table."""

    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User table."""

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
