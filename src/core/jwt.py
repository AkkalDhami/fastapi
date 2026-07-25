from datetime import datetime, timedelta, timezone

from jose import jwt

from configs import settings

ACCESS_TOKEN_EXPIRE = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE = 7  # 7 days


def create_access_token(
    data: dict,
):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    payload.update(
        {
            "exp": expire,
            "type": "access",
        }
    )

    return jwt.encode(
        payload,
        settings.JWT_ACCESS_SECRET,
        algorithm="HS256",
    )


def create_refresh_token(
    data: dict,
):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE)

    payload.update(
        {
            "exp": expire,
            "type": "refresh",
        }
    )

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET,
        algorithm="HS256",
    )


from jose import JWTError

from core.exceptions import UnauthorizedException

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"


def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        
        print("Token verified", payload=payload)

        if payload.get("type") != "access":
            raise UnauthorizedException("Invalid token type")

        return payload

    except JWTError:
        raise UnauthorizedException("Invalid or expired token")
