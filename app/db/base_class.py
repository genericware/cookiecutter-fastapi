# Standard Library ---------------------------------------------------------------------
from typing import Any

# Third-Party --------------------------------------------------------------------------
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class definition."""

    id: Any
