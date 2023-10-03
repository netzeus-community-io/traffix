from datetime import datetime, timedelta
from jose import jwt, JWTError
from traffix.config import settings


def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """Creates a JSON Web Token (JWT) with a specific expiration time

    Args:
        expires_delta:  timedelta object to overide default expiration timer
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.JWT_EXPIRE)

    payload = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        claims=payload,
        key=settings.JWT_SHARED_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decodes a Token

    Args:
        token:      Token string
    """
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SHARED_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as err:
        return None
    except Exception as err:
        return None

    return payload
