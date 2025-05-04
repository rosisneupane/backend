from fastapi import APIRouter, Request, Form, Depends,Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import User
from models.emergency_alert_model import EmergencyAlert
from models.video_model import Collection,Video
from models.media_model import Media
from starlette.status import HTTP_302_FOUND
from fastapi.templating import Jinja2Templates
from utils.security import verify_password, create_access_token
from middleware.auth_middleware import get_current_user,get_current_user_admin
from schemas.auth_schema import UserResponse
from uuid import UUID

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")  # Ensure you have a 'templates' folder

@router.get("/", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@router.post("/login")
async def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email, User.is_admin == True).first()
    print(user)
    
    if user and verify_password(password, user.hashed_password):  # Replace with password hashing check
        response = RedirectResponse(url="/admin/dashboard", status_code=HTTP_302_FOUND)
        token = create_access_token(data={"sub": user.id,"is_admin":True})
        response.set_cookie(
            key="admin_token",
            value=token,
            httponly=True,  # Prevents JavaScript access (more secure)
            samesite="Lax",
            max_age=60 * 60 * 24  # 1 day expiration
        )
        return response

    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid credentials"})

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request,current_user: str =  Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})


# Users Page Route
@router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()  # Fetch users from DB
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users})

# Videos Page Route
@router.get("/videos", response_class=HTMLResponse)
async def admin_videos(request: Request, db: Session = Depends(get_db)):
    collections = db.query(Collection).all()
    return templates.TemplateResponse("admin_videos.html", {
        "request": request,
        "collections": collections
    })

@router.get("/emergency-alerts", response_class=HTMLResponse)
async def admin_emergency_alerts(request: Request, db: Session = Depends(get_db)):
    alerts = db.query(EmergencyAlert).order_by(EmergencyAlert.timestamp.desc()).all()
    return templates.TemplateResponse("admin_emergency_alerts.html", {
        "request": request,
        "alerts": alerts
    })

@router.get("/media", response_class=HTMLResponse)
def admin_media_page(request: Request, db: Session = Depends(get_db)):
    media_items = db.query(Media).all()
    return templates.TemplateResponse("admin_media.html", {
        "request": request,
        "media_items": media_items
    })


CATEGORIES = ["self-care", "wrok", "social", "leisure", "education"]

@router.get("/media/add", response_class=HTMLResponse)
def show_add_media_form(request: Request):
    return templates.TemplateResponse("add_media.html", {
        "request": request,
        "categories": CATEGORIES
    })

@router.get("/collections/add", response_class=HTMLResponse)
async def add_collection_form(request: Request):
    return templates.TemplateResponse("add_collection.html", {"request": request})

@router.get("/videos/add", response_class=HTMLResponse)
async def add_video_form(request: Request, collection_id: UUID = Query(None)):
    return templates.TemplateResponse("add_video.html", {"request": request, "collection_id": collection_id})




