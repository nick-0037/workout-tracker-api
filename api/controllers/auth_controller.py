from fastapi import APIRouter, Depends, status
from api.models.user import UserCreate, UserResponse, UserLogin, Token
from api.services.auth_service import AuthService
from api.dependencies.repositories import get_auth_repo
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


async def get_service(user_repo=Depends(get_auth_repo)):
    """Dependency to inject the service with repository and DB."""
    return AuthService(user_repository=user_repo)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account and returns the newly created user information.",
    responses={
        409: {"description": "Email already registered"},
    },
)
async def register(user: UserCreate, service: AuthService = Depends(get_service)):
    return await service.create_user(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate a user",
    description="Validates user credentials and returns a JWT access token if correct.",
    responses={
        401: {"description": "Invalid email or password"},
    },
)
async def login(credentials: UserLogin, service: AuthService = Depends(get_service)):
    return await service.login(credentials)


@router.post(
    "/login/oauth",
    response_model=Token,
    summary="Authenticate a user (OAuth2 Form)",
    description="Validates user credentials (Form Data) and returns a JWT access token. Used by Swagger UI.",
    responses={
        401: {"description": "Invalid email or password"},
    },
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_service),
):
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return await service.login(credentials)
