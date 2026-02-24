from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..database import Base


class PasswordResetCode(Base):
    """密码重置验证码"""
    __tablename__ = "password_reset_codes"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), nullable=True, index=True)
    email = Column(String(100), nullable=True, index=True)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
