from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User
from ..models.community import TreatmentSolution
from ..schemas.solution import SolutionCreate, SolutionResponse
from ..utils.security import get_current_user

router = APIRouter(prefix="/solutions", tags=["治疗方案"])

@router.get("", response_model=List[SolutionResponse])
def list_solutions(
    disease: Optional[str] = Query(None, description="按疾病筛选，如：糖尿病、高血压"),
    db: Session = Depends(get_db)
):
    """用户侧：仅返回已通过审核的方案，支持按疾病筛选"""
    q = (
        db.query(TreatmentSolution)
        .filter(TreatmentSolution.status == TreatmentSolution.STATUS_APPROVED)
    )
    if disease and disease.strip():
        q = q.filter(TreatmentSolution.disease_name == disease.strip())
    items = q.order_by(TreatmentSolution.updated_at.desc()).all()
    return items

@router.get("/{solution_id}", response_model=SolutionResponse)
def get_solution(solution_id: int, db: Session = Depends(get_db)):
    """用户侧：方案详情（仅已通过）"""
    item = db.query(TreatmentSolution).filter(
        TreatmentSolution.id == solution_id,
        TreatmentSolution.status == TreatmentSolution.STATUS_APPROVED
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="方案不存在或未上线")
    return item

@router.post("", response_model=SolutionResponse)
def create_solution(
    data: SolutionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """患者新建方案，状态为待审核"""
    solution = TreatmentSolution(
        title=data.title,
        disease_name=data.disease_name,
        category=data.category or "综合方案",
        description=data.description or "",
        success_rate=data.success_rate,
        user_count=data.user_count or 0,
        status=TreatmentSolution.STATUS_PENDING,
        created_by_id=current_user.id,
    )
    db.add(solution)
    db.commit()
    db.refresh(solution)
    return solution
