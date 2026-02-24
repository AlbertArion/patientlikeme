from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    """更新个人信息，所有字段可选"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    """忘记密码 - 请求验证码"""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class ForgotPasswordReset(BaseModel):
    """忘记密码 - 重置"""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    code: str
    new_password: str
