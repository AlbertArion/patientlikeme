"""为 treatment_solutions 添加 treatment_methods_json 字段并填充示例数据"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "patient_community.db")

# 按方案/疾病预设的治疗手段分类示例（参考 PatientsLikeMe）
SOLUTION_METHODS = {
    1: [  # 糖尿病 - 综合管理方案
        {"category": "处方药", "name": "二甲双胍", "patient_count": 892},
        {"category": "处方药", "name": "胰岛素", "patient_count": 654},
        {"category": "非处方药", "name": "阿司匹林", "patient_count": 120},
        {"category": "补充剂", "name": "维生素D", "patient_count": 98},
        {"category": "营养/饮食", "name": "低糖饮食", "patient_count": 450},
        {"category": "练习", "name": "有氧运动", "patient_count": 380},
        {"category": "生活方式改变", "name": "规律监测血糖", "patient_count": 520},
    ],
    2: [  # 高血压 - 降压治疗方案
        {"category": "处方药", "name": "氨氯地平", "patient_count": 456},
        {"category": "处方药", "name": "缬沙坦", "patient_count": 389},
        {"category": "非处方药", "name": "阿司匹林", "patient_count": 104},
        {"category": "营养/饮食", "name": "低盐饮食", "patient_count": 320},
        {"category": "练习", "name": "步行", "patient_count": 280},
        {"category": "生活方式改变", "name": "戒烟限酒", "patient_count": 198},
    ],
    3: [  # 慢性肾病 - 肾功能保护方案
        {"category": "处方药", "name": "ACEI/ARB", "patient_count": 156},
        {"category": "营养/饮食", "name": "低蛋白饮食", "patient_count": 89},
        {"category": "补充剂", "name": "活性维生素D", "patient_count": 67},
        {"category": "物理治疗", "name": "康复锻炼", "patient_count": 45},
    ],
    4: [  # 冠心病 - 心血管康复方案
        {"category": "处方药", "name": "阿司匹林", "patient_count": 312},
        {"category": "处方药", "name": "他汀类", "patient_count": 298},
        {"category": "处方药", "name": "β受体阻滞剂", "patient_count": 245},
        {"category": "物理治疗", "name": "心脏康复", "patient_count": 178},
        {"category": "练习", "name": "有氧运动", "patient_count": 156},
        {"category": "手术", "name": "支架植入", "patient_count": 89},
        {"category": "心理治疗", "name": "心理疏导", "patient_count": 67},
    ],
    5: [  # 类风湿关节炎 - 关节保护方案
        {"category": "处方药", "name": "甲氨蝶呤", "patient_count": 234},
        {"category": "处方药", "name": "生物制剂", "patient_count": 156},
        {"category": "非处方药", "name": "布洛芬", "patient_count": 98},
        {"category": "物理治疗", "name": "关节功能锻炼", "patient_count": 112},
        {"category": "补充和替代医学", "name": "热敷/理疗", "patient_count": 87},
    ],
    6: [  # 哮喘 - 呼吸管理方案
        {"category": "处方药", "name": "吸入性糖皮质激素", "patient_count": 345},
        {"category": "处方药", "name": "沙丁胺醇", "patient_count": 217},
        {"category": "处方药", "name": "孟鲁司特", "patient_count": 134},
        {"category": "设备", "name": "峰流速仪", "patient_count": 89},
        {"category": "生活方式改变", "name": "避免过敏原", "patient_count": 156},
    ],
}


def migrate():
    if not os.path.exists(DB_PATH):
        print("数据库不存在，跳过迁移")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(treatment_solutions)")
    cols = {row[1] for row in cur.fetchall()}
    if "treatment_methods_json" not in cols:
        cur.execute("ALTER TABLE treatment_solutions ADD COLUMN treatment_methods_json TEXT")
        print("已添加 treatment_methods_json 列")
    for sid, methods in SOLUTION_METHODS.items():
        cur.execute(
            "UPDATE treatment_solutions SET treatment_methods_json = ? WHERE id = ?",
            (json.dumps(methods, ensure_ascii=False), sid),
        )
    updated = cur.rowcount
    conn.commit()
    conn.close()
    print("已更新方案的治疗手段分类数据")


if __name__ == "__main__":
    migrate()
