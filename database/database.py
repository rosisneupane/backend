from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "sqlite:///./users.db"  # SQLite DB file
DATABASE_URL = "postgresql://rosis_database_user:n6fjcRQAMnfGHZpT3jGkmruhR3OF2rnC@dpg-d0i4t956ubrc73d62lm0-a.oregon-postgres.render.com/rosis_database"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
