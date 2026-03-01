import os

__database_name = os.getenv("DATABASE_NAME")
database_path = f"sqlite+aiosqlite:///{__database_name}"
