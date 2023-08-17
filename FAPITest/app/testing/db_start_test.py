import os
import sys

from sqlalchemy import text
sys.path.append(os.getcwd())
# import 

from app.database import SessionLocal


def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise e

def main() -> None:
    init()

if __name__ == "__main__":
    main()