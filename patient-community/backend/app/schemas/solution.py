import json
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime


class TreatmentMethodItem(BaseModel):
    category: str
    name: str
    patient_count: int = 0

class SolutionCreate(BaseModel):
    """患者新建方案"""
    title: str = Field(..., min_length=1, max_length=200)
    disease_name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field("综合方案", max_length=50)
    description: str = Field("", max_length=2000)
    success_rate: Optional[str] = Field(None, max_length=20)
    user_count: Optional[int] = Field(0, ge=0)

class SolutionUpdate(BaseModel):
    """运营更新方案（可部分字段）"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    disease_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    success_rate: Optional[str] = Field(None, max_length=20)
    user_count: Optional[int] = Field(None, ge=0)

class SolutionResponse(BaseModel):
    """用户侧展示（仅已通过）"""
    id: int
    title: str
    disease_name: str
    category: Optional[str] = None
    description: Optional[str]
    success_rate: Optional[str]
    user_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    treatment_methods: Optional[List[TreatmentMethodItem]] = None

    @field_validator("treatment_methods", mode="before")
    @classmethod
    def parse_treatment_methods(cls, v: Any):
        if v is None:
            return None
        if isinstance(v, str):
            if not v.strip():
                return None
            try:
                data = json.loads(v)
                return [TreatmentMethodItem(**x) for x in data] if isinstance(data, list) else None
            except Exception:
                return None
        if isinstance(v, list):
            return [TreatmentMethodItem(**x) if isinstance(x, dict) else x for x in v]
        return v

    class Config:
        from_attributes = True

class SolutionAdminResponse(SolutionResponse):
    """运营侧列表/详情（含状态与审核信息）"""
    status: str
    created_by_id: Optional[int]
    updated_at: Optional[datetime]
    reviewed_at: Optional[datetime]
    reject_reason: Optional[str]

    class Config:
        from_attributes = True

class SolutionReviewBody(BaseModel):
    """审核操作"""
    action: str = Field(..., description="approve | reject")
    reject_reason: Optional[str] = Field(None, max_length=500)
