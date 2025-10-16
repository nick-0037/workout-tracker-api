import pytest
from unittest.mock import AsyncMock, Mock
from api.models.user import UserCreate, UserResponse, UserLogin, Token
from api.services.auth_service import AuthService
from fastapi import HTTPException
from api.utils.security import hash_password


class TestAuthService:
    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_user_repository):
        # Arrange
        user_data = UserCreate(
            username="newuser",
            email="new@example.com",
            password="securepass123"
        )
        
        expected_user = UserResponse(
            id=1,
            username="newuser",
            email="new@example.com"
        )
        
        mock_user_repository.get_user_by_email = AsyncMock(return_value=None)
        mock_user_repository.create_user = AsyncMock(return_value=expected_user)
        
        auth_service = AuthService(mock_user_repository)
        
        # Act
        result = await auth_service.create_user(user_data)
        
        # Assert
        assert result.username == "newuser"
        assert result.email == "new@example.com"
        mock_user_repository.get_user_by_email.assert_called_once_with("new@example.com")
        mock_user_repository.create_user.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email_fails(self, mock_user_repository):
        # Arrange
        user_data = UserCreate(
            username="duplicate",
            email="exists@example.com",
            password="pass123"
        )
        
        existing_user = UserResponse(
            id=1,
            username="duplicate",
            email="exists@example.com",
        )
        
        mock_user_repository.get_user_by_email = AsyncMock(return_value=existing_user)
        auth_service = AuthService(mock_user_repository)
        
        # Act
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.create_user(user_data)
            
        # Assert
        assert exc_info.value.status_code == 400
        assert "already registered" in str(exc_info.value.detail).lower()
    
    @pytest.mark.asyncio
    async def test_login_success(self, mock_user_repository):
        # Arrange
        password = "correctpass"
        password_hash = hash_password(password)
        credentials = UserLogin(
            email="user@example.com",
            password=password
        )
        
        stored_user = Mock()
        stored_user.id = 1
        stored_user.email = "user@example.com"
        stored_user.password_hash = password_hash
        
        mock_user_repository.get_user_by_email = AsyncMock(return_value=stored_user)
        auth_service = AuthService(mock_user_repository)
        
        # Act
        result = await auth_service.login(credentials)
        
        # Assert
        assert isinstance(result, Token)
        assert result.token_type == "bearer"
        assert len(result.access_token) > 0
        
    @pytest.mark.asyncio
    async def test_login_invalid_credentials_fails(self, mock_user_repository):
        # Arrange
        credentials = UserLogin(
            email="user@example.com",
            password="wrongpass"
        )
        
        mock_user_repository.get_user_by_email = AsyncMock(return_value=None)
        auth_service = AuthService(mock_user_repository)
        
        # Act
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login(credentials)
        
        # Assert
        assert exc_info.value.status_code == 401
        