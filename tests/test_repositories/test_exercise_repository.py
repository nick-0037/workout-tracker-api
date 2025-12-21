import pytest
import pytest_asyncio

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
async def test_get_all_exercises_success(
    test_db_session, real_exercise_repo, setup_test_user
):
    # Arrange
    user_id = setup_test_user

    await test_db_session.execute(
        """
        INSERT INTO exercises (user_id, name, description, category, muscle_group)
        VALUES (?, 'Push Up', 'A basic push up exercise', 'Strength', 'Chest'),
        (?, 'Pull Up', 'A basic pull up exercise', 'Strength', 'Back')
        """,
        (user_id, user_id),
    )

    await test_db_session.commit()

    # Act
    exercises = await real_exercise_repo.get_all_exercises(user_id=user_id)

    # Assert
    assert len(exercises) == 2
    assert exercises[0]["name"] == "Push Up"
    assert exercises[1]["name"] == "Pull Up"


@pytest.mark.asyncio
async def test_get_exercise_by_id_found(
    test_db_session, real_exercise_repo, setup_test_user
):
    # Arrange
    user_id = setup_test_user

    await test_db_session.execute(
        """
        INSERT INTO exercises (id, user_id, name, description, category, muscle_group)
        VALUES (1, ?, 'Push Up',  'A basic push up exercise', 'Strength', 'Chest')
        """,
        (user_id,),
    )

    await test_db_session.commit()

    # Act
    exercise = await real_exercise_repo.get_exercise_by_id(
        exercise_id=1, user_id=user_id
    )

    # Assert
    assert exercise is not None
    assert exercise["id"] == 1
    assert exercise["name"] == "Push Up"


@pytest.mark.asyncio
async def test_get_exercise_by_id_not_found(
    test_db_session, real_exercise_repo, setup_test_user
):
    # Act
    exercise = await real_exercise_repo.get_exercise_by_id(
        exercise_id=99, user_id=setup_test_user
    )

    # Assert
    assert exercise is None
