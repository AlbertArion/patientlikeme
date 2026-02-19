from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.medical_record import MedicalRecord, MedicalInfo
from ..models.user import User
from typing import List, Dict

def calculate_similarity(info1: MedicalInfo, info2: MedicalInfo) -> float:
    """计算两个病历的相似度"""
    score = 0.0
    
    # 疾病名称匹配（权重40%）
    if info1.disease_name and info2.disease_name:
        if info1.disease_name.lower() == info2.disease_name.lower():
            score += 0.4
        elif info1.disease_name.lower() in info2.disease_name.lower() or \
             info2.disease_name.lower() in info1.disease_name.lower():
            score += 0.2
    
    # 症状相似度（权重30%）
    if info1.symptoms and info2.symptoms:
        symptoms1 = set(info1.symptoms.lower().split())
        symptoms2 = set(info2.symptoms.lower().split())
        if symptoms1 and symptoms2:
            common = len(symptoms1 & symptoms2)
            total = len(symptoms1 | symptoms2)
            score += 0.3 * (common / total if total > 0 else 0)
    
    # 治疗方案相似度（权重30%）
    if info1.treatment_plan and info2.treatment_plan:
        plan1 = set(info1.treatment_plan.lower().split())
        plan2 = set(info2.treatment_plan.lower().split())
        if plan1 and plan2:
            common = len(plan1 & plan2)
            total = len(plan1 | plan2)
            score += 0.3 * (common / total if total > 0 else 0)
    
    return score

def find_similar_patients(db: Session, user_id: int, limit: int = 10) -> List[Dict]:
    """查找相似患者"""
    # 获取当前用户的病历信息
    user_records = db.query(MedicalRecord).filter(
        and_(
            MedicalRecord.user_id == user_id,
            MedicalRecord.is_processed == True
        )
    ).all()
    
    if not user_records:
        return []
    
    # 获取用户的病历信息
    user_infos = []
    for record in user_records:
        if record.medical_info:
            user_infos.append(record.medical_info)
    
    if not user_infos:
        return []
    
    # 获取所有其他用户的已处理病历
    other_records = db.query(MedicalRecord).filter(
        and_(
            MedicalRecord.user_id != user_id,
            MedicalRecord.is_processed == True
        )
    ).all()
    
    # 计算相似度
    similarities = []
    for other_record in other_records:
        if not other_record.medical_info:
            continue
        
        # 与用户的每个病历计算相似度，取最高值
        max_similarity = 0.0
        for user_info in user_infos:
            similarity = calculate_similarity(user_info, other_record.medical_info)
            max_similarity = max(max_similarity, similarity)
        
        if max_similarity > 0.1:  # 相似度阈值
            user = db.query(User).filter(User.id == other_record.user_id).first()
            if user:
                similarities.append({
                    "user_id": user.id,
                    "username": user.username,
                    "avatar": user.avatar,
                    "disease_name": other_record.medical_info.disease_name,
                    "similarity": round(max_similarity * 100, 2)
                })
    
    # 按相似度排序
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    
    return similarities[:limit]
