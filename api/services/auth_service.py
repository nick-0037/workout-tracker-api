from api.models.user import UserCreate, UserResponse, UserLogin, Token
from api.utils.security import hash_password
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from api.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if exists
        existing_user = await self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash pass
        hashed_password = hash_password(user_data.password)

        # Call repository to save user
        user = await self.user_repository.create_user(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
        )

        return user

    async def login(self, credentials: UserLogin) -> Token:
        user = await self.user_repository.get_user_by_email(credentials.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # check password
        password = hash_password(credentials.password)
        if user.password_hash != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Create JWT
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return Token(access_token=access_token)
