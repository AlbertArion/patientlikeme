from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from ..models.user import User
from ..utils.security import get_current_user
from ..services.match_service import find_similar_patients

router = APIRouter(prefix="/match", tags=["患者匹配"])

@router.get("/similar", response_model=List[Dict])
def get_similar_patients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取相似患者"""
    similar_patients = find_similar_patients(db, current_user.id)
    return similar_patients

@router.get("/recommendations")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取推荐治疗方案"""
    # 这里可以根据用户病历推荐治疗方案
    # 简化实现，返回示例数据
    return {
        "recommendations": [
            {
                "id": 1,
                "title": "综合治疗方案",
                "description": "结合药物治疗和物理治疗",
                "success_rate": "85%",
                "user_count": 120
            }
        ]
    }
