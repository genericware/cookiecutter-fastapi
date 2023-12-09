from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    """Base model properties."""

    title: str | None = None
    description: str | None = None


class ItemCreate(ItemBase):
    """Create model properties."""

    title: str


class ItemUpdate(ItemBase):
    """Update model properties."""

    pass


class ItemInDBBase(ItemBase):
    """Database base model properties."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    owner_id: UUID

class Item(ItemInDBBase):
    """Database model properties."""

    pass


class ItemInDB(ItemInDBBase):
    """In database model properties."""

    pass
