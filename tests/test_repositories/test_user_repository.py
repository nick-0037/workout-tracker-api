import pytest
import pytest_asyncio
import sqlite3


@pytest_asyncio.fixture
async def setup_test_user(test_db_session):
    await test_db_session.execute(
        """
        INSERT OR IGNORE INTO users (id, username, email, password_hash)
        VALUES (1, 'test_user', 'testuser@example.com', 'hashed_pass')
        """
    )

    await test_db_session.commit()

    return 1


@pytest.mark.asyncio
async def test_create_user_success(test_db_session, real_user_repo):
    # Act
    user = await real_user_repo.create_user(
        username="test_user", email="testuser@example.com", password_hash="hashed_pass"
    )

    # Assert
    assert user["username"] == "test_user"
    assert "id" in user

    cursor = await test_db_session.execute(
        "SELECT * FROM users WHERE email = 'testuser@example.com'"
    )
    row = await cursor.fetchone()
    assert row is not None
    assert row["username"] == "test_user"


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email_fails(real_user_repo, setup_test_user):
    # Act & Assert
    with pytest.raises(sqlite3.IntegrityError) as exc_info:
        await real_user_repo.create_user(
            username="testuser2", email="testuser@example.com", password_hash="any_hash"
        )

    assert "UNIQUE constraint failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_by_email_returns_user_when_exists(
    real_user_repo, setup_test_user
):
    # Act
    user = await real_user_repo.get_user_by_email("testuser@example.com")

    # Assert
    assert user is not None
    assert user["username"] == "test_user"
    assert user["email"] == "testuser@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email_returns_none_when_not_exists(real_user_repo):
    # Act
    user = await real_user_repo.get_user_by_email("nonexistent@example.com")

    # Assert
    assert user is None
