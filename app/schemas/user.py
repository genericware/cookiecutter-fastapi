# Standard Library ---------------------------------------------------------------------
import uuid

# Third-Party --------------------------------------------------------------------------
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Read model properties."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Create model properties."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Update model properties."""

    pass
