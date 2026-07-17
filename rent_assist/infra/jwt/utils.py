"""JWT token generation and validation utilities"""

import datetime
import logging
from typing import Any
from uuid import UUID

import jwt
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError

logger = logging.getLogger(__name__)


class JWTUtils:
    """Utility class for JWT token operations"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_access_token(
        self,
        user_id: UUID,
        roles: list[str],
        expires_in_seconds: int = 3600,
    ) -> str:
        now = datetime.datetime.utcnow()
        payload = {
            "sub": str(user_id),
            "roles": roles,
            "type": "access",
            "iat": now,
            "exp": now + datetime.timedelta(seconds=expires_in_seconds),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def generate_refresh_token(
        self,
        user_id: UUID,
        session_id: UUID,
        expires_in_days: int = 30,
    ) -> str:
        now = datetime.datetime.utcnow()
        payload = {
            "sub": str(user_id),
            "session_id": str(session_id),
            "type": "refresh",
            "iat": now,
            "exp": now + datetime.timedelta(days=expires_in_days),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError as e:
            logger.warning("Token has expired")
            raise ValueError("Token has expired") from e
        except DecodeError as e:
            logger.warning("Invalid token format")
            raise ValueError("Invalid token") from e
        except InvalidTokenError as e:
            logger.warning(f"Token validation failed: {e}")
            raise ValueError(f"Token validation failed: {e}") from e

    def get_user_id_from_token(self, token: str) -> UUID:
        payload = self.decode_token(token)
        return UUID(payload["sub"])

    def hash_token(self, token: str) -> str:
        import hashlib

        return hashlib.sha256(token.encode()).hexdigest()
