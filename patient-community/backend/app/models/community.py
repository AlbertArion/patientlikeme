from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class Community(Base):
    __tablename__ = "communities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    member_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TreatmentSolution(Base):
    """治疗方案：患者可新建，需审核通过后用户侧才展示"""
    __tablename__ = "treatment_solutions"

    # 状态：pending=待审核, approved=已通过, rejected=已拒绝
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    id = Column(Integer, primary_key=True, index=True)
    disease_name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=True, default="综合方案")  # 处方药/非处方药/补充剂/综合方案/康复治疗等
    description = Column(Text, nullable=True)
    success_rate = Column(String(20), nullable=True)  # 如 "85%"
    user_count = Column(Integer, default=0)
    status = Column(String(20), default=STATUS_PENDING, nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reject_reason = Column(Text, nullable=True)
    treatment_methods_json = Column(Text, nullable=True)  # JSON: [{"category":"处方药","name":"阿司匹林","patient_count":104}, ...]

    @property
    def treatment_methods(self):
        if not self.treatment_methods_json:
            return None
        try:
            import json
            return json.loads(self.treatment_methods_json)
        except Exception:
            return None
