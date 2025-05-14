from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "sqlite:///./users.db"  # SQLite DB file
DATABASE_URL = "postgresql://rosis_db_user:t52mT7O5m7hrJp8QtStPH9V6ITVUlu3W@dpg-d0i41l6mcj7s739m8rh0-a.oregon-postgres.render.com/rosis_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
