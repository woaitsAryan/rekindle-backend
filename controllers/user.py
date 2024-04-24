from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from helpers.db import get_db
from middleware.protect import protect
from models.user import User

userRouter = APIRouter()

@userRouter.post("/") 
def get_user(db: Session = Depends(get_db), id: str = Depends(protect)):
    existing_user = db.query(User).filter(User.id == id).first()
    if existing_user == None:
        raise HTTPException(
            status_code=400,
            detail="User with this email, phone already exists",
    )
    return {
        "name": existing_user.name,
        "created_on": existing_user.created_on
    }