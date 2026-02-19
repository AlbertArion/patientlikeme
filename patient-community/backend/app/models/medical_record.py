from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(Boolean, default=False)
    
    # 关系
    medical_info = relationship("MedicalInfo", back_populates="record", uselist=False)

class MedicalInfo(Base):
    __tablename__ = "medical_info"
    
    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False, unique=True)
    disease_name = Column(String(100), nullable=True)
    symptoms = Column(Text, nullable=True)
    diagnosis_date = Column(Date, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    record = relationship("MedicalRecord", back_populates="medical_info")
