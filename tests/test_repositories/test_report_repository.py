import pytest

@pytest.mark.asyncio
async def test_get_report_summary_success(test_db_session, real_report_repo):
    # Arrange
    db_conn = test_db_session

    await db_conn.executescript(
        """
        INSERT OR IGNORE INTO users (id, username, email, password_hash) 
        VALUES (1, 'test_user', 'test@example.com', 'hashed');
        
        INSERT INTO workout_plans (id, user_id, name, description) VALUES (1, 1, 'Plan Test', 'Desc');
        INSERT INTO exercises (id, user_id, name, category) VALUES (1, 1, 'Squat', 'Strength');
        INSERT INTO exercises (id, user_id, name, category) VALUES (2, 1, 'Bench Press', 'Strength');
    """
    )

    await db_conn.executescript(
        """
        -- COMPLETED SESSIONS (Should be counted: Total 2 Sessions)
        INSERT INTO workout_sessions (id, workout_plan_id, user_id, scheduled_date, status) 
        VALUES (10, 1, 1, '2025-12-01 10:00:00', 'completed');
        INSERT INTO workout_sessions (id, workout_plan_id, user_id, scheduled_date, status) 
        VALUES (11, 1, 1, '2025-12-02 11:00:00', 'completed');

        -- PENDING SESSION (Should NOT be counted if SQL is correct)
        INSERT INTO workout_sessions (id, workout_plan_id, user_id, scheduled_date, status) 
        VALUES (12, 1, 1, '2025-12-03 12:00:00', 'pending');
        
        -- EXERCISES (Total 4 records: 2 in Session 10, 1 in Session 11, 1 in Session 12)
        
        -- Session 10 Data (2 exercises)
        INSERT INTO sessions_exercises (session_id, exercise_id, reps_completed, weight_used) VALUES (10, 1, 10, 50.0);
        INSERT INTO sessions_exercises (session_id, exercise_id, reps_completed, weight_used) VALUES (10, 2, 20, 150.0);
        
        -- Session 11 Data (1 exercise)
        INSERT INTO sessions_exercises (session_id, exercise_id, reps_completed, weight_used) VALUES (11, 1, 15, 100.0);
        
        -- Session 12 Data (1 exercise)
        INSERT INTO sessions_exercises (session_id, exercise_id, reps_completed, weight_used) VALUES (12, 2, 5, 10.0);
    """
    )

    await db_conn.commit()

    # Act
    summary = await real_report_repo.get_summary(user_id=1)

    # Assert
    assert isinstance(summary, dict)
    assert summary["total_sessions"] == 2
    assert summary["total_exercises"] == 4
    # avg_reps: (10 + 20 + 15 + 5) = 45 / 4 = 12.5
    assert summary["avg_reps"] == 12.5
    # avg_weight: (50.0 + 150.0 + 100.0 + 10.0) = 300.0 / 4 = 77.5
    assert summary["avg_weight"] == 77.5
