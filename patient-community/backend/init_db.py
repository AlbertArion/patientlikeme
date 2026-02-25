"""
数据库初始化脚本
创建数据库表并插入初始数据
"""
from app.database import engine, SessionLocal, Base
from app.models import User, Community, TreatmentSolution
from app.utils.security import get_password_hash

def init_database():
    """初始化数据库"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")
    
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        if db.query(User).first():
            print("数据库已有数据，跳过初始化")
            return
        
        print("插入初始数据...")
        
        # 创建测试用户
        test_user = User(
            username="testuser",
            email="test@example.com",
            phone="13800138000",
            password_hash=get_password_hash("123456")
        )
        db.add(test_user)
        
        # 创建社区
        communities = [
            Community(name="癌症社区", description="为癌症患者提供支持和交流", member_count=0),
            Community(name="糖尿病社区", description="糖尿病患者的健康管理和经验分享", member_count=0),
            Community(name="心血管疾病社区", description="心血管疾病患者的康复交流", member_count=0),
            Community(name="肾病社区", description="肾病患者的治疗经验分享", member_count=0),
            Community(name="罕见病社区", description="罕见病患者的互助平台", member_count=0),
        ]
        db.add_all(communities)
        
        # 创建治疗方案（初始为已通过，便于用户侧展示）- 6 种预制方案
        solutions = [
            TreatmentSolution(
                disease_name="糖尿病",
                title="综合管理方案",
                category="综合方案",
                description="包括饮食控制、运动疗法和药物治疗的综合方案，通过科学的血糖管理和生活方式调整，有效控制糖尿病进展。",
                success_rate="85%",
                user_count=150,
                status=TreatmentSolution.STATUS_APPROVED
            ),
            TreatmentSolution(
                disease_name="高血压",
                title="降压治疗方案",
                category="药物治疗",
                description="通过药物和生活方式调整控制血压，包括合理用药、低盐饮食、适量运动等综合措施。",
                success_rate="90%",
                user_count=200,
                status=TreatmentSolution.STATUS_APPROVED
            ),
            TreatmentSolution(
                disease_name="慢性肾病",
                title="肾功能保护方案",
                category="综合方案",
                description="延缓肾功能衰退的综合治疗方案，包括药物治疗、饮食管理和定期监测。",
                success_rate="75%",
                user_count=80,
                status=TreatmentSolution.STATUS_APPROVED
            ),
            TreatmentSolution(
                disease_name="冠心病",
                title="心血管康复方案",
                category="康复治疗",
                description="通过药物治疗、运动康复和心理干预，改善心血管功能，预防心血管事件。",
                success_rate="82%",
                user_count=120,
                status=TreatmentSolution.STATUS_APPROVED
            ),
            TreatmentSolution(
                disease_name="类风湿关节炎",
                title="关节保护方案",
                category="康复治疗",
                description="综合运用药物治疗、物理治疗和功能锻炼，减轻关节炎症，保护关节功能。",
                success_rate="78%",
                user_count=95,
                status=TreatmentSolution.STATUS_APPROVED
            ),
            TreatmentSolution(
                disease_name="哮喘",
                title="呼吸管理方案",
                category="药物治疗",
                description="通过规范化的药物治疗和环境控制，有效控制哮喘症状，提高生活质量。",
                success_rate="88%",
                user_count=160,
                status=TreatmentSolution.STATUS_APPROVED
            ),
        ]
        db.add_all(solutions)
        
        db.commit()
        print("初始数据插入完成")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
