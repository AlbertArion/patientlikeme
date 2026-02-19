from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class MedicalInfoBase(BaseModel):
    disease_name: Optional[str] = None
    symptoms: Optional[str] = None
    diagnosis_date: Optional[date] = None
    treatment_plan: Optional[str] = None
    medications: Optional[str] = None

class MedicalInfoResponse(MedicalInfoBase):
    id: int
    record_id: int
    extracted_at: datetime
    
    class Config:
        from_attributes = True

class MedicalRecordBase(BaseModel):
    title: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    user_id: int
    file_path: str
    file_type: str
    upload_time: datetime
    is_processed: bool
    medical_info: Optional[MedicalInfoResponse] = None
    
    class Config:
        from_attributes = True
