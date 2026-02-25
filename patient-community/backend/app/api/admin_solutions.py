from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from ..database import get_db
from ..models.community import TreatmentSolution
from ..schemas.solution import SolutionUpdate, SolutionAdminResponse, SolutionReviewBody
from ..utils.security import require_admin_key

router = APIRouter(prefix="/admin/solutions", tags=["运营-治疗方案"], dependencies=[Depends(require_admin_key)])

@router.get("", response_model=List[SolutionAdminResponse])
def admin_list_solutions(
    status_filter: Optional[str] = Query(None, description="pending | approved | rejected"),
    db: Session = Depends(get_db)
):
    """运营端：方案列表，可按状态筛选"""
    q = db.query(TreatmentSolution).order_by(TreatmentSolution.created_at.desc())
    if status_filter and status_filter in (
        TreatmentSolution.STATUS_PENDING,
        TreatmentSolution.STATUS_APPROVED,
        TreatmentSolution.STATUS_REJECTED,
    ):
        q = q.filter(TreatmentSolution.status == status_filter)
    return q.all()

@router.get("/{solution_id}", response_model=SolutionAdminResponse)
def admin_get_solution(solution_id: int, db: Session = Depends(get_db)):
    """运营端：方案详情"""
    item = db.query(TreatmentSolution).filter(TreatmentSolution.id == solution_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="方案不存在")
    return item

@router.put("/{solution_id}", response_model=SolutionAdminResponse)
def admin_update_solution(
    solution_id: int,
    data: SolutionUpdate,
    db: Session = Depends(get_db)
):
    """运营端：更新方案信息（不改变审核状态）"""
    item = db.query(TreatmentSolution).filter(TreatmentSolution.id == solution_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="方案不存在")
    update = data.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item

@router.post("/{solution_id}/review", response_model=SolutionAdminResponse)
def admin_review_solution(
    solution_id: int,
    body: SolutionReviewBody,
    db: Session = Depends(get_db)
):
    """运营端：审核通过或拒绝"""
    item = db.query(TreatmentSolution).filter(TreatmentSolution.id == solution_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="方案不存在")
    if item.status != TreatmentSolution.STATUS_PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该方案已审核，无法重复操作")
    now = datetime.now(timezone.utc)
    if body.action == "approve":
        item.status = TreatmentSolution.STATUS_APPROVED
        item.reject_reason = None
    elif body.action == "reject":
        item.status = TreatmentSolution.STATUS_REJECTED
        item.reject_reason = body.reject_reason or ""
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="action 须为 approve 或 reject")
    item.reviewed_at = now
    db.commit()
    db.refresh(item)
    return item
