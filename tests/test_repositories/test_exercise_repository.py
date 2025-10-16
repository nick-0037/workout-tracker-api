import pytest
from api.models.exercise import ExerciseCreate, ExerciseResponse
from api.repositories.exercise_repository import ExerciseRepository

@pytest.mark.asyncio
async def test_get_all_exercises_return_list(test_db):
    # Arrange
    repo = ExerciseRepository(test_db)
    
    # Act
    exercises = await repo.get_all_exercises()
    
    # Assert
    assert isinstance(exercises, list)
    assert len(exercises) > 0
    assert all(isinstance(ex, ExerciseResponse) for ex in exercises)

@pytest.mark.asyncio
async def test_get_all_exercises_empty_db(test_db):
    # Arrange
    repo = ExerciseRepository(test_db)
    
    test_db.execute("DELETE FROM exercises")  # Clear the table for this test
    test_db.commit()
    
    # Act
    exercises = await repo.get_all_exercises()
    
    # Assert
    assert isinstance(exercises, list)
    assert len(exercises) == 0    

@pytest.mark.asyncio
async def test_get_exercise_by_id_returns_exercise(test_db):
    # Arrange
    repo = ExerciseRepository(test_db)
    
    cursor = test_db.execute(
        "INSERT INTO exercises (name, description, category, muscle_group) VALUES (?, ?, ?, ?)",
        ("Push Up", "A basic push up exercise", "Strength", "Chest"),
    )
    test_db.commit()
    exercise_id = cursor.lastrowid
    
    # Act
    exercise = await repo.get_exercise_by_id(exercise_id)
    
    # Assert
    assert exercise is not None
    assert isinstance(exercise, ExerciseResponse)
    assert exercise.id == exercise_id
    assert exercise.name == "Push Up"
    assert exercise.description == "A basic push up exercise"

@pytest.mark.asyncio
async def test_get_exercise_by_id_not_found(test_db):
    # Arrange
    repo = ExerciseRepository(test_db)
    
    # Act
    exercise = await repo.get_exercise_by_id(12)
    
    # Assert
    assert exercise is None
    