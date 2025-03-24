from fastapi import FastAPI
from controllers.auth_controller import router as auth_router
from database.database import Base, engine


# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

app.include_router(auth_router)
