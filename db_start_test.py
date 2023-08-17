from sqlalchemy import text
from db.base import SessionLocal


def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        # Clean db for new values
        db.execute(text('drop schema public cascade;'))
        db.execute(text('create schema public;'))
        db.commit()
    except Exception as e:
        raise e

def main() -> None:
    init()

if __name__ == "__main__":
    main()