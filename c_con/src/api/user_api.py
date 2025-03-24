from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.service.user_service.user_service import UserService
from src.schemas.user_schema import UserCreate,UserUpdate, UserResponse

user_router = APIRouter(prefix="/api/users")



@user_router.get("/{user_name}/", response_model=UserResponse)
async def get_user_by_id(user_name: str, db: Session = Depends(get_db)):
    sevice = UserService(db)
    db_user = sevice.get_user_by_username(user_name)
    print(db_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.get("/all/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users in the database.

    Returns:
        list[UserResponse]: A list of all users in the database.
    """
    sevice = UserService(db)
    users = sevice.get_all_users()
    print(users)
    return users


@user_router.post("/new_user/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
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


@user_router.put("/update_user/", response_model=bool)
async def update_user(user: UserUpdate, db: Session = Depends(get_db)):
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
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    


@user_router.delete("/delete_user/", response_model=bool)
async def delete_user(user_name: str, db: Session = Depends(get_db)):
    sevice = UserService(db)
    db_user = sevice.delete_user(user_name)
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

    