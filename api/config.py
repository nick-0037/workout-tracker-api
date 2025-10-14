from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV")
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

DB_PATH = ":memory:" if ENV == "test" else os.getenv("DB_PATH", "database/app.db")