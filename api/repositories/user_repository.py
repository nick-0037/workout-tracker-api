from api.models.user import UserResponse
from api.utils.security import hash_password
from typing import Optional


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def create_user(
        self, username: str, email: str, password: str
    ) -> UserResponse:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hash_password(password)),
        )
        self.db.commit()
        user_id = cursor.lastrowid
        return UserResponse(id=user_id, username=username, email=email)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT id, username, email FROM users WHERE email = ?", (email,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        user = UserResponse(
            id=row[0],
            username=row[1],
            email=row[2],
        )

        return user
