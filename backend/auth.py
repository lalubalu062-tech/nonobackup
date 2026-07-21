from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "NONO_HUB_SECRET_2026"
ALGORITHM = "HS256"


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_token(data):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=7)

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    data = decode_token(token)

    return data
