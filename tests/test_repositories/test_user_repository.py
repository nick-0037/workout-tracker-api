import pytest
from api.models.user import UserCreate, UserResponse
from api.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user_inserts_into_db(test_db):
    # Arrange
    repo = UserRepository(test_db)

    # Act
    user = await repo.create_user(
        username="testuser", email="test@example.com", password="pass123"
    )

    # Assert
    assert isinstance(user, UserResponse)
    assert user.username == "testuser"
    assert user.email == "test@example.com"

    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'testuser'")
    row = cursor.fetchone()
    assert row is not None


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email_fails(test_db):
    # Arrange
    repo = UserRepository(test_db)
    await repo.create_user(
        username="testuser1",
        email="duplicate@example.com",
        password="pass123",
    )

    # Act & Assert
    with pytest.raises(Exception):
        await repo.create_user(
            username="testuser2",
            email="duplicate@example.com",
            password="pass123",
        )

@pytest.mark.asyncio
async def test_get_user_by_email_returns_user_when_exists(test_db):
    # Arrange
    repo = UserRepository(test_db)
    test_db.execute(
		"INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
		("john", "john@example.com", "pass123")
	)
    test_db.commit()
    
    # Act
    user = await repo.get_user_by_email("john@example.com")
    
    # Assert
    assert user is not None
    assert user.username == "john"
    assert user.email == "john@example.com"
    
@pytest.mark.asyncio
async def test_get_user_by_email_returns_none_when_not_exists(test_db):
    # Arrange
    repo = UserRepository(test_db)
    
    # Act
    user = await repo.get_user_by_email("nonexistent@example.com")
    
    # Assert
    assert user is None
    
# Additional tests can be added for edge cases and error handling
    
    