import random
import string
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.password_reset import PasswordResetCode
from ..schemas.user import (
    UserCreate, UserLogin, UserResponse, UserUpdate, Token,
    ForgotPasswordRequest, ForgotPasswordReset
)
from ..utils.security import verify_password, get_password_hash, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if user_data.email and db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查手机号是否已存在
    if user_data.phone and db.query(User).filter(User.phone == user_data.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已被注册"
        )
    
    # 创建新用户
    user = User(
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 查找用户（支持用户名、邮箱、手机号登录）
    user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.username) |
        (User.phone == user_data.username)
    ).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户信息（仅邮箱、手机号）"""
    if user_data.email is not None:
        existing = db.query(User).filter(User.email == user_data.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被其他用户使用")
        current_user.email = user_data.email
    if user_data.phone is not None:
        existing = db.query(User).filter(User.phone == user_data.phone, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="手机号已被其他用户使用")
        current_user.phone = user_data.phone

    db.commit()
    db.refresh(current_user)
    return current_user


def _generate_code() -> str:
    return "".join(random.choices(string.digits, k=6))


@router.post("/forgot-password/request")
def forgot_password_request(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """忘记密码 - 请求验证码（支持手机号或邮箱）"""
    if not data.phone and not data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请填写手机号或邮箱"
        )
    # 查找用户
    if data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该手机号未注册")
    else:
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该邮箱未注册")

    # 删除该账号之前的验证码
    if data.phone:
        db.query(PasswordResetCode).filter(PasswordResetCode.phone == data.phone).delete()
    else:
        db.query(PasswordResetCode).filter(PasswordResetCode.email == data.email).delete()

    code = _generate_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    reset_code = PasswordResetCode(
        phone=data.phone,
        email=data.email,
        code=code,
        expires_at=expires_at
    )
    db.add(reset_code)
    db.commit()

    # 生产环境应通过短信/邮件发送验证码，此处为演示返回验证码
    return {
        "message": "验证码已发送",
        "code": code
    }


@router.post("/forgot-password/reset")
def forgot_password_reset(data: ForgotPasswordReset, db: Session = Depends(get_db)):
    """忘记密码 - 验证码重置密码"""
    if not data.phone and not data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请填写手机号或邮箱"
        )
    if len(data.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码至少6位"
        )

    # 查找验证码
    if data.phone:
        reset_record = db.query(PasswordResetCode).filter(
            PasswordResetCode.phone == data.phone,
            PasswordResetCode.code == data.code
        ).first()
    else:
        reset_record = db.query(PasswordResetCode).filter(
            PasswordResetCode.email == data.email,
            PasswordResetCode.code == data.code
        ).first()

    if not reset_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码错误")
    if datetime.utcnow() > reset_record.expires_at:
        db.delete(reset_record)
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="验证码已过期，请重新获取")

    # 查找用户并更新密码
    if data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()
    else:
        user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    user.password_hash = get_password_hash(data.new_password)
    db.delete(reset_record)
    db.commit()

    return {"message": "密码重置成功"}
