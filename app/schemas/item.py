from uuid import UUID

from pydantic import BaseModel


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

    id: int
    title: str
    owner_id: UUID

    class Config:
        orm_mode = True


class Item(ItemInDBBase):
    """Database model properties."""

    pass


class ItemInDB(ItemInDBBase):
    """In database model properties."""

    pass
