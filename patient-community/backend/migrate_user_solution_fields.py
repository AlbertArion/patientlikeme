"""添加 users.interested_conditions 和 treatment_solutions.category 字段（可重复执行）"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "patient_community.db")

def migrate():
    if not os.path.exists(DB_PATH):
        print("数据库不存在，跳过迁移")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # users.interested_conditions
    cur.execute("PRAGMA table_info(users)")
    user_cols = {row[1] for row in cur.fetchall()}
    if "interested_conditions" not in user_cols:
        try:
            cur.execute("ALTER TABLE users ADD COLUMN interested_conditions TEXT")
            print("已添加 users.interested_conditions")
        except sqlite3.OperationalError as e:
            print(f"添加 interested_conditions 失败: {e}")
    else:
        print("users.interested_conditions 已存在，跳过")

    # treatment_solutions.category
    cur.execute("PRAGMA table_info(treatment_solutions)")
    sol_cols = {row[1] for row in cur.fetchall()}
    if "category" not in sol_cols:
        try:
            cur.execute("ALTER TABLE treatment_solutions ADD COLUMN category TEXT DEFAULT '综合方案'")
            print("已添加 treatment_solutions.category")
            cur.execute(
                "UPDATE treatment_solutions SET category = '综合方案' WHERE category IS NULL"
            )
            cur.execute(
                "UPDATE treatment_solutions SET category = '药物治疗' WHERE disease_name IN ('高血压','哮喘')"
            )
            cur.execute(
                "UPDATE treatment_solutions SET category = '康复治疗' WHERE disease_name IN ('冠心病','类风湿关节炎')"
            )
        except sqlite3.OperationalError as e:
            print(f"添加 category 失败: {e}")
    else:
        print("treatment_solutions.category 已存在，跳过")

    conn.commit()
    conn.close()
    print("迁移完成")

if __name__ == "__main__":
    migrate()
