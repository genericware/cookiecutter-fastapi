from fastapi import APIRouter

from app.api.v1.endpoints import items
from app.config import APIPrefix, APITags, settings
from app.db.users import auth_backend, fastapi_users, oauth_client
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix=APIPrefix.v1)
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"{APIPrefix.auth.value}/jwt",
    tags=[APITags.auth],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=APIPrefix.auth,
    tags=[APITags.auth],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=APIPrefix.auth,
    tags=[APITags.auth],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=APIPrefix.auth,
    tags=[APITags.auth],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=APIPrefix.users,
    tags=[APITags.users],
)
router.include_router(
    fastapi_users.get_oauth_router(
        oauth_client, auth_backend, settings.fastapi_secret_key
    ),
    prefix=f"{APIPrefix.auth.value}/oauth",
    tags=[APITags.auth],
)
router.include_router(items.router, prefix=APIPrefix.items, tags=[APITags.items])
