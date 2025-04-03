from sqlalchemy.orm import Session
from database.database import engine
from models.user_model import User
import uuid

def promote_user_to_admin(user_id: str):
    session = Session(bind=engine)
    try:
        user = session.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user:
            print("User not found.")
            return
        
        user.is_admin = True
        session.commit()
        print(f"User {user.username} is now an admin.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    user_id = input("Enter user ID to promote: ")
    promote_user_to_admin(user_id)
