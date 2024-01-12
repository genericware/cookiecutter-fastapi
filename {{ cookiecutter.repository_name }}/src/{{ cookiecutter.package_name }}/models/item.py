from typing import TYPE_CHECKING

from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401, isort:skip


class Item(Base):
    """Item database model."""

    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(UUID, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
