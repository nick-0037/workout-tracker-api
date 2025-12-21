from typing import Optional, Dict


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def create_user(self, username: str, email: str, password_hash: str) -> Dict:
        cursor = await self.db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        await self.db.commit()
        user_id = cursor.lastrowid
        await cursor.close()
        return {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
        }

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        cursor = await self.db.execute(
            "SELECT id, username, email, password_hash FROM users WHERE email = ?",
            (email,),
        )
        row = await cursor.fetchone()
        await cursor.close()

        if not row:
            return None

        return dict(row)
