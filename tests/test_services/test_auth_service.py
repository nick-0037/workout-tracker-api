import pytest
from unittest.mock import AsyncMock
from api.models.user import UserCreate, UserResponse, UserLogin, Token
from api.services.auth_service import AuthService
from api.utils.security import hash_password
from api.core.error_handler import AppException


@pytest.fixture
def auth_service(mock_user_repository):
    return AuthService(mock_user_repository)


@pytest.mark.asyncio
async def test_create_user_success(auth_service, mock_user_repository):
    # Arrange
    user_data = UserCreate(
        username="newuser", email="new@example.com", password="securepass123"
    )

    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.create_user.return_value = UserResponse(
        id=1, username="newuser", email="new@example.com"
    )

    # Act
    result = await auth_service.create_user(user_data)

    # Assert
    assert result.username == "newuser"
    assert result.email == "new@example.com"

    mock_user_repository.get_user_by_email.assert_called_once_with("new@example.com")
    mock_user_repository.create_user.assert_called_once()

    _, kwargs = mock_user_repository.create_user.call_args

    assert kwargs["password_hash"] != user_data.password
    assert "password_hash" in kwargs


@pytest.mark.asyncio
async def test_create_user_duplicate_email_fails(auth_service, mock_user_repository):
    # Arrange
    user_data = UserCreate(
        username="duplicate", email="exists@example.com", password="pass123"
    )

    mock_user_repository.get_user_by_email.return_value = UserResponse(
        id=1,
        username="duplicate",
        email="exists@example.com",
    )

    # Act
    with pytest.raises(AppException) as exc_info:
        await auth_service.create_user(user_data)

    # Assert
    assert exc_info.value.code == 409
    assert "already registered" in exc_info.value.message.lower()


@pytest.mark.asyncio
async def test_login_success(auth_service, mock_user_repository):
    # Arrange
    password = "correctpass"
    hashed = hash_password(password)

    credentials = UserLogin(email="user@example.com", password=password)

    stored_user = AsyncMock()
    stored_user.id = 1
    stored_user.email = "user@example.com"
    stored_user.password_hash = hashed

    mock_user_repository.get_user_by_email.return_value = stored_user

    # Act
    result = await auth_service.login(credentials)

    # Assert
    assert isinstance(result, Token)
    assert result.token_type == "bearer"
    assert len(result.access_token) > 0


@pytest.mark.asyncio
async def test_login_invalid_credentials_fails(auth_service, mock_user_repository):
    # Arrange
    credentials = UserLogin(email="user@example.com", password="wrongpass")

    mock_user_repository.get_user_by_email.return_value = None

    # Act
    with pytest.raises(AppException) as exc_info:
        await auth_service.login(credentials)

    # Assert
    assert exc_info.value.code == 401
