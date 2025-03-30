from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.service.user_service.user_service import UserService
from src.service.session_service.session_service import SessionService
from src.schemas.user_schema import UserLogin, UserResponse, UserUpdate, UserCreate
import uuid

user_router = APIRouter( prefix="/api/users", tags=["api/users"])

@user_router.post("/login/", summary="Login", response_model=UserResponse)
async def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        session_service = SessionService(db)

        db_user = user_service.login_user(user.username, user.password)
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = str(uuid.uuid4())
        session_service.create_session(db_user.user_id, session_id)

        response.set_cookie(key="session_id", value=session_id, httponly=True)

        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_router.get("/profile/", response_model=UserResponse)
async def get_user_profile(request: Request, db: Session = Depends(get_db)):
    try:
        session_service = SessionService(db)

        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        user_id = session_service.validate_session(session_id)
        if not user_id:
            raise HTTPException(status_code=401, detail="Session expired or invalid")

        user_service = UserService(db)
        db_user = user_service.get_user_by_username(user_id)

        return db_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@user_router.get("/all/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users in the database.

    Returns:
        list[UserResponse]: A list of all users in the database.
    """
    try:
        sevice = UserService(db)
        users = sevice.get_all_users()
        return users
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@user_router.put("/forgot_password/", response_model=UserResponse)
async def forgot_password(user: UserLogin, db: Session = Depends(get_db)):
    try:
        sevice = UserService(db)
        username = user.username
        password = user.password
        db_user = sevice.forgot_password(username, password)
        return db_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
@user_router.post("/register/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    try:
        sevice = UserService(db)
        username = user.username
        email = user.email
        password = user.password
        name = user.name
        phone_number = user.phone_number
        role = user.role
        created_at = user.created_at


        db_user = sevice.create_user(username, email, password, name, phone_number, role, created_at)
        return db_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_router.put("/update_user/", response_model=bool)
async def update_user(user: UserUpdate, db: Session = Depends(get_db)):
    try:
        sevice = UserService(db)
        # id = user.id
        username = user.username
        email = user.email
        password = user.password
        name = user.name
        phone_number = user.phone_number
        role = user.role
        created_at = user.created_at

        db_user = sevice.update_user( username, email, password, name, phone_number, role, created_at)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user_router.delete("/delete_user/", response_model=bool)
async def delete_user(user_name: str, db: Session = Depends(get_db)):
    
    
    try:    
        sevice = UserService(db)
        db_user = sevice.delete_user(user_name)
        return db_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    