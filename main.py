from fastapi import FastAPI
from controllers.auth_controller import router as auth_router
from controllers.routine_controller import router as routine_router
from controllers.mood_controller import router as mood_router
from controllers.admin_controller import router as admin_router
from controllers.conversation_controller import router as conversation_router
from controllers.ai_conversation_controller import router as ai_conversation_router
from controllers.message_controller import router as message_router
from controllers.user_controller import router as user_router
from controllers.video_controller import router as video_router
from controllers.collection_controller import router as collection_router
from controllers.media_controller import router as pdf_router
from controllers.event_controller import router as event_router
from database.database import Base, engine
from fastapi.staticfiles import StaticFiles
import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dqlba0s8j",
    api_key="963721232975944",
    api_secret="tFIbgxfmzyg0NGgUq_AHKFOxY-I"
)



# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(routine_router)
app.include_router(mood_router)
app.include_router(conversation_router)
app.include_router(ai_conversation_router)
app.include_router(message_router)
app.include_router(collection_router)
app.include_router(video_router)
app.include_router(pdf_router)
app.include_router(event_router)
app.include_router(admin_router)  # Admin route