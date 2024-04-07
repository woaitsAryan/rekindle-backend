from pydantic import BaseModel, EmailStr, Field


class EmotionModel(BaseModel):
    text: str

class RegisterModel(BaseModel):
    name: str
    password: str = Field(..., min_length=8)
    email: EmailStr

class LoginModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    
