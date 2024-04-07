from datetime import timedelta
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

from helpers.db import get_db
from models.schema import LoginModel, RegisterModel
from models.user import User
from helpers.auth import authenticate_user, create_access_token, get_password_hash

authRouter = APIRouter()

@authRouter.post("/login")
async def login(form_data: LoginModel, db: Session = Depends(get_db)):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"token": access_token}

@authRouter.post("/signup") 
async def create_user(user: RegisterModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email, phone already exists",
    )
    hashed_password = get_password_hash(user.password)
    user_dict = user.model_dump()
    user_dict.pop('password', None)
    new_user = User(
        **user_dict,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )
    
    return {"token": access_token}