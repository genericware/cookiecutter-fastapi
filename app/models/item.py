# Third-Party --------------------------------------------------------------------------
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Project ------------------------------------------------------------------------------
from app.db.base_class import Base


class Item(Base):
    """Item database model."""

    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
