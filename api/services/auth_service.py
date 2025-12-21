from api.models.user import UserCreate, UserResponse, UserLogin, Token
from api.utils.security import hash_password, verify_password
from datetime import datetime, timedelta, timezone
from jose import jwt
from api.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from api.core.error_handler import AppException


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if exists
        existing_user = await self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise AppException("Email already registered", 409)

        # Hash pass
        password_hash = hash_password(user_data.password)

        # Call repository to save user
        user = await self.user_repository.create_user(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
        )

        return user

    async def login(self, credentials: UserLogin) -> Token:
        user = await self.user_repository.get_user_by_email(credentials.email)

        if not user:
            raise AppException("Invalid credentials", 401)

        # check password
        if not verify_password(credentials.password, user.password_hash):
            raise AppException("Invalid credentials", 401)

        # Create JWT
        token_data = {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return Token(access_token=access_token)
