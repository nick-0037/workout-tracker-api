from fastapi import APIRouter, Depends, status
from api.models.user import UserCreate, UserResponse, UserLogin, Token
from api.services.auth_service import AuthService
from database.db import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate, db=Depends(get_db)):
    service = AuthService(db)
    return await service.create_user(user)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db=Depends(get_db)):
    service = AuthService(db)
    return await service.login(credentials)
