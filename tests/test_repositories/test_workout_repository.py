import pytest
from api.models.workout_plan import WorkoutPlanResponse
from api.models.workout_plan_exercise import WorkoutPlanExerciseResponse
from api.repositories.workout_repository import WorkoutRepository


@pytest.mark.asyncio
async def test_get_all_workout_plans_returns_all_for_user(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    
    await repo.create_workout_plan(
        user_id=1,
        name="Push Day",
    )
    
    await repo.create_workout_plan(
        user_id=1,
        name="Pull Day"
    )

    # Act
    workout_plans = await repo.get_all_workout_plans(user_id=1)

    # Assert
    assert isinstance(workout_plans, list)
    assert len(workout_plans) == 2
    assert all(isinstance(wk, WorkoutPlanResponse) for wk in workout_plans)
    names = [wk.name for wk in workout_plans]
    assert "Push Day" in names
    assert "Pull Day" in names

@pytest.mark.asyncio
async def test_get_workout_plan_by_id_return_successfully(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    
    created_workout = await repo.create_workout_plan(
        user_id=1,
        name= "Push Day"
    )
    
    # Act & Assert
    workout_plan = await repo.get_workout_plan_by_id(created_workout.id, user_id=1)
    
    assert isinstance(workout_plan, WorkoutPlanResponse)
    assert workout_plan.id == created_workout.id
    assert workout_plan.user_id == 1
    assert workout_plan.name == "Push Day"
    
@pytest.mark.asyncio
async def test_create_workout_plan_inserts_into_db(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    
    # Act
    workout_plan = await repo.create_workout_plan(
        user_id=1,
        name="Legs Day",
        description="Legs description"
    )
    
    # Assert
    assert isinstance(workout_plan, WorkoutPlanResponse)
    assert workout_plan.name == "Legs Day"
    assert workout_plan.description == "Legs description"
    
    cursor = test_db.execute(
        "SELECT * FROM workout_plans WHERE name = ?", ("Legs Day",)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == 1


@pytest.mark.asyncio
async def test_update_workout_plan_updates_fields_successfully(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    created_plan = await repo.create_workout_plan(
        user_id=1,
        name="Legs Day"
    )
    
    # Act 
    updated_workout = await repo.update_workout_plan(
        workout_plan_id=created_plan.id,
        user_id=1,
        name="Updated Legs Day",
        description="Updated workout for legs"
    )
    
    # Assert
    assert isinstance(updated_workout, WorkoutPlanResponse)
    assert updated_workout.name == "Updated Legs Day"
    assert updated_workout.description == "Updated workout for legs"
    
    cursor = test_db.execute(
        "SELECT name, description FROM workout_plans WHERE id = ?", (created_plan.id,)
    )
    
    row = cursor.fetchone()
    assert row[0] == "Updated Legs Day"
    assert row[1] == "Updated workout for legs"
    
@pytest.mark.asyncio
async def test_delete_workout_plan_removes_from_db(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    
    created_workout = await repo.create_workout_plan(
        user_id=1,
        name="Push Day",
    )
    
    # Act
    deleted_workout = await repo.delete_workout_plan(
        workout_plan_id=created_workout.id,
        user_id=1
    )
    
    # Assert
    assert deleted_workout is True
    
    cursor = test_db.execute(
        "SELECT * FROM workout_plans WHERE id = ?", (created_workout.id,)
    )
    
    row = cursor.fetchone()
    assert row is None
    
@pytest.mark.asyncio
async def test_add_exercise_to_plan_inserts_into_db(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    
    created_workout = await repo.create_workout_plan(
        user_id=1,
        name="Legs Day"
    )
    
    # Act
    exercise = await repo.add_exercise_to_plan(
        workout_plan_id=created_workout.id,
        exercise_id=1,
        sets=3,
        reps=10,
        weight=50.0
    )
    
    # Assert
    assert isinstance(exercise, WorkoutPlanExerciseResponse)
    assert exercise.workout_plan_id == created_workout.id
    assert exercise.exercise_id == 1
    assert exercise.sets == 3
    
    cursor = test_db.execute(
        "SELECT * FROM workout_plan_exercises WHERE workout_plan_id = ?", (created_workout.id,)
    )
    row = cursor.fetchone()
    assert row is not None
    
@pytest.mark.asyncio
async def test_remove_exercise_from_plan_successfully(test_db):
    # Arrange
    repo = WorkoutRepository(test_db)
    
    created_workout = await repo.create_workout_plan(
        user_id=1,
        name="Legs Day"
    )
    
    await repo.add_exercise_to_plan(
        workout_plan_id=created_workout.id,
        exercise_id=1,
        sets=3,
        reps=10,
        weight=50.0
    )
    
    # Act
    exercise = await repo.remove_exercise_from_plan(
        workout_plan_id=created_workout.id,
        exercise_id=1
    )
    
    # Assert
    assert exercise is True
    
    cursor = test_db.execute(
        "SELECT * FROM workout_plan_exercises WHERE workout_plan_id = ? AND exercise_id = ?", (created_workout.id, 1)
    )
    row = cursor.fetchone()
    assert row is None
    