from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from ..database import get_db
from ..models.user import User
from ..models.medical_record import MedicalRecord, MedicalInfo
from ..schemas.medical_record import MedicalRecordResponse
from ..utils.security import get_current_user
from ..utils.file_handler import save_upload_file, delete_file
from ..services.ai_service import extract_medical_info

router = APIRouter(prefix="/records", tags=["病历管理"])

@router.post("/upload", response_model=MedicalRecordResponse)
async def upload_record(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传病历"""
    try:
        # 保存文件
        file_path = save_upload_file(file)
        file_ext = os.path.splitext(file.filename)[1]
        
        # 创建病历记录
        record = MedicalRecord(
            user_id=current_user.id,
            title=file.filename,
            file_path=file_path,
            file_type=file_ext,
            is_processed=False
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败: {str(e)}"
        )

@router.get("", response_model=List[MedicalRecordResponse])
def get_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取病历列表"""
    records = db.query(MedicalRecord).filter(
        MedicalRecord.user_id == current_user.id
    ).order_by(MedicalRecord.upload_time.desc()).all()
    
    return records

@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_record_detail(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取病历详情"""
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id,
        MedicalRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="病历不存在"
        )
    
    return record

@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除病历"""
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id,
        MedicalRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="病历不存在"
        )
    
    # 删除文件
    delete_file(record.file_path)
    
    # 删除数据库记录
    db.delete(record)
    db.commit()
    
    return {"message": "删除成功"}

@router.post("/{record_id}/process", response_model=MedicalRecordResponse)
async def process_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """处理病历（AI提取信息）"""
    record = db.query(MedicalRecord).filter(
        MedicalRecord.id == record_id,
        MedicalRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="病历不存在"
        )
    
    if record.is_processed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="病历已处理"
        )
    
    try:
        # 使用AI提取信息
        extracted_info = await extract_medical_info(record.file_path, record.file_type)
        
        # 保存提取的信息
        medical_info = MedicalInfo(
            record_id=record.id,
            disease_name=extracted_info.get("disease_name"),
            symptoms=extracted_info.get("symptoms"),
            diagnosis_date=extracted_info.get("diagnosis_date"),
            treatment_plan=extracted_info.get("treatment_plan"),
            medications=extracted_info.get("medications")
        )
        
        db.add(medical_info)
        
        # 更新处理状态
        record.is_processed = True
        
        db.commit()
        db.refresh(record)
        
        return record
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理失败: {str(e)}"
        )
