# Import all the models, so that Base has them before being
# imported by Alembic
from src.app.db.base_class import Base  # noqa: F401
from src.app.models.item import Item  # noqa: F401
from src.app.models.user import User  # noqa: F401
