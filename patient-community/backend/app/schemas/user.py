import json
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    interested_conditions: Optional[List[str]] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    """更新个人信息，所有字段可选"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    interested_conditions: Optional[List[str]] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    created_at: datetime

    @field_validator('interested_conditions', mode='before')
    @classmethod
    def parse_interested_conditions(cls, v):
        if isinstance(v, str):
            return json.loads(v) if v else None
        return v
    
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
