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


@pytest_asyncio.fixture
async def test_plan(test_db_session, setup_test_user):
    user_id = setup_test_user
    cursor = await test_db_session.execute(
        "INSERT INTO workout_plans (user_id, name, description) VALUES (?, ?, ?)",
        (user_id, "Base Plan", "Base Description"),
    )
    plan_id = cursor.lastrowid
    await test_db_session.commit()
    return plan_id


@pytest_asyncio.fixture
async def test_exercise(test_db_session, setup_test_user):
    user_id = setup_test_user

    cursor = await test_db_session.execute("SELECT id FROM exercises LIMIT 1")

    row = await cursor.fetchone()

    if not row:
        cursor = await test_db_session.execute(
            """
            INSERT INTO exercises (user_id, name, description, category, muscle_group)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, "Sample Exercise", "Description", "Strength", "Full Body"),
        )

        await test_db_session.commit()
        return cursor.lastrowid

    return row["id"]


@pytest.mark.asyncio
async def test_get_all_workout_plans_success(
    test_db_session, real_workout_repo, setup_test_user
):
    # Arrange
    user_id = setup_test_user

    await test_db_session.execute(
        """
        INSERT INTO workout_plans (id, user_id, name, description)
        VALUES (1, ?, 'Push Day', NULL),
               (2, ?, 'Pull Day', NULL)
        """,
        (user_id, user_id),
    )

    await test_db_session.commit()

    # Act
    workout_plans = await real_workout_repo.get_all_workout_plans(user_id=user_id)

    # Assert
    assert len(workout_plans) == 2
    names = [wk["name"] for wk in workout_plans]
    assert "Push Day" in names
    assert "Pull Day" in names


@pytest.mark.asyncio
async def test_get_workout_plan_by_id_success(
    test_db_session, real_workout_repo, setup_test_user
):
    # Arrange
    user_id = setup_test_user

    await test_db_session.execute(
        """
        INSERT INTO workout_plans (id, user_id, name, description)
        VALUES (1, ?, 'Push Day', NULL)
        """,
        (user_id,),
    )

    await test_db_session.commit()

    # Act
    workout_plan = await real_workout_repo.get_workout_plan_by_id(
        workout_plan_id=1, user_id=user_id
    )

    # Assert
    assert workout_plan["id"] == 1
    assert workout_plan["user_id"] == 1
    assert workout_plan["name"] == "Push Day"


@pytest.mark.asyncio
async def test_create_workout_plan_success(real_workout_repo, setup_test_user):
    # Arrange
    user_id = setup_test_user

    # Act
    workout_plan = await real_workout_repo.create_workout_plan(
        user_id=user_id, name="Legs Day", description="Legs description"
    )

    # Assert
    assert workout_plan["name"] == "Legs Day"
    assert workout_plan["description"] == "Legs description"


@pytest.mark.asyncio
async def test_update_workout_plan_success(
    test_db_session, real_workout_repo, setup_test_user
):
    # Arrange
    user_id = setup_test_user

    cursor = await test_db_session.execute(
        """
        INSERT INTO workout_plans (user_id, name, description)
        VALUES (?, 'Legs Day', 'Workout for legs')
        """,
        (user_id,),
    )
    await test_db_session.commit()
    plan_id = cursor.lastrowid

    # Act
    updated_workout = await real_workout_repo.update_workout_plan(
        workout_plan_id=plan_id,
        user_id=user_id,
        name="Updated Legs Day",
        description="Updated workout for legs",
    )

    # Assert
    assert updated_workout is not None
    assert updated_workout["id"] == plan_id
    assert updated_workout["name"] == "Updated Legs Day"
    assert updated_workout["description"] == "Updated workout for legs"


@pytest.mark.asyncio
async def test_delete_workout_plan_success(
    test_db_session, real_workout_repo, setup_test_user
):
    # Arrange
    user_id = setup_test_user

    cursor = await test_db_session.execute(
        """
        INSERT INTO workout_plans (user_id, name, description)
        VALUES (?, 'Cardio Day', 'Cardio des')
        """,
        (user_id,),
    )
    await test_db_session.commit()
    plan_id = cursor.lastrowid

    # Act
    deleted_workout = await real_workout_repo.delete_workout_plan(
        workout_plan_id=plan_id, user_id=user_id
    )

    # Assert
    assert deleted_workout is True


@pytest.mark.asyncio
async def test_add_exercise_to_plan_success(
    real_workout_repo, test_plan, test_exercise
):
    # Arrange
    plan_id = test_plan
    ex_base_id = test_exercise

    # Act
    exercise = await real_workout_repo.add_exercise_to_plan(
        workout_plan_id=plan_id, exercise_id=ex_base_id, sets=3, reps=10, weight=50.0
    )

    # Assert
    assert exercise["workout_plan_id"] == plan_id
    assert exercise["exercise_id"] == ex_base_id
    assert "exercise_name" in exercise
    assert exercise["sets"] == 3


@pytest.mark.asyncio
async def test_remove_exercise_from_plan_success(
    real_workout_repo, test_plan, test_exercise
):
    # Arrange
    plan_id = test_plan
    ex_base_id = test_exercise

    await real_workout_repo.add_exercise_to_plan(
        workout_plan_id=plan_id, exercise_id=ex_base_id, sets=3, reps=10, weight=50.0
    )

    # Act
    exercise = await real_workout_repo.remove_exercise_from_plan(
        workout_plan_id=plan_id, exercise_id=ex_base_id
    )

    # Assert
    assert exercise is True
