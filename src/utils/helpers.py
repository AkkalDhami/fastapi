from fastapi import Cookie

from core.exceptions import UnauthorizedException
from core.jwt import verify_access_token


def get_current_user_id(
    access_token: str | None = Cookie(default=None),
) -> int:
    if not access_token:
        raise UnauthorizedException("Not authenticated")

    payload = verify_access_token(access_token)

    return int(payload["sub"])
