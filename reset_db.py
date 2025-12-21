from api.config import DB_PATH
import os

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"🗑️  Removed existing database at {DB_PATH}")
else:
    print(f"ℹ️  No existing database found at {DB_PATH}")

from database.db import main
main()