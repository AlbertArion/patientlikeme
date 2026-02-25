"""补充缺失的预制治疗方案（已有数据库可执行，已存在则跳过）"""
from app.database import SessionLocal
from app.models.community import TreatmentSolution

SEED_SOLUTIONS = [
    {"disease_name": "糖尿病", "title": "综合管理方案", "description": "包括饮食控制、运动疗法和药物治疗的综合方案，通过科学的血糖管理和生活方式调整，有效控制糖尿病进展。", "success_rate": "85%", "user_count": 150},
    {"disease_name": "高血压", "title": "降压治疗方案", "description": "通过药物和生活方式调整控制血压，包括合理用药、低盐饮食、适量运动等综合措施。", "success_rate": "90%", "user_count": 200},
    {"disease_name": "慢性肾病", "title": "肾功能保护方案", "description": "延缓肾功能衰退的综合治疗方案，包括药物治疗、饮食管理和定期监测。", "success_rate": "75%", "user_count": 80},
    {"disease_name": "冠心病", "title": "心血管康复方案", "description": "通过药物治疗、运动康复和心理干预，改善心血管功能，预防心血管事件。", "success_rate": "82%", "user_count": 120},
    {"disease_name": "类风湿关节炎", "title": "关节保护方案", "description": "综合运用药物治疗、物理治疗和功能锻炼，减轻关节炎症，保护关节功能。", "success_rate": "78%", "user_count": 95},
    {"disease_name": "哮喘", "title": "呼吸管理方案", "description": "通过规范化的药物治疗和环境控制，有效控制哮喘症状，提高生活质量。", "success_rate": "88%", "user_count": 160},
]


def seed_solutions():
    db = SessionLocal()
    try:
        existing = {(s.disease_name, s.title) for s in db.query(TreatmentSolution).filter(TreatmentSolution.status == TreatmentSolution.STATUS_APPROVED).all()}
        added = 0
        for item in SEED_SOLUTIONS:
            key = (item["disease_name"], item["title"])
            if key in existing:
                continue
            s = TreatmentSolution(**item, status=TreatmentSolution.STATUS_APPROVED)
            db.add(s)
            added += 1
        db.commit()
        print(f"已补充 {added} 个预制治疗方案，当前共 {len(existing) + added} 个")
    except Exception as e:
        print(f"补充失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_solutions()
