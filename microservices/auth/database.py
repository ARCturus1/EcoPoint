from dotenv import load_dotenv
import os

load_dotenv()

__database_name = os.getenv("DATABASE_NAME")
database_path = f"sqlite+aiosqlite:///{__database_name}"
