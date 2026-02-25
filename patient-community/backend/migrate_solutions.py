"""为 treatment_solutions 表添加审核相关字段（可重复执行，已存在则跳过）"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "patient_community.db")
COLUMNS = [
    ("status", "TEXT DEFAULT 'pending' NOT NULL"),
    ("created_by_id", "INTEGER REFERENCES users(id)"),
    ("updated_at", "DATETIME"),
    ("reviewed_at", "DATETIME"),
    ("reject_reason", "TEXT"),
]

def migrate():
    if not os.path.exists(DB_PATH):
        print("数据库不存在，首次运行 create_all 时会创建新表，无需迁移")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(treatment_solutions)")
    existing = {row[1] for row in cur.fetchall()}
    for name, spec in COLUMNS:
        if name in existing:
            print(f"列 {name} 已存在，跳过")
            continue
        try:
            cur.execute(f"ALTER TABLE treatment_solutions ADD COLUMN {name} {spec}")
            print(f"已添加列: {name}")
        except sqlite3.OperationalError as e:
            print(f"添加 {name} 失败: {e}")
    # 仅将从未审核过的旧记录设为已通过（reviewed_at 为空），保证用户侧列表仍可见
    cur.execute(
        "UPDATE treatment_solutions SET status = 'approved' WHERE (status IS NULL OR status = '' OR status = 'pending') AND reviewed_at IS NULL"
    )
    if cur.rowcount:
        print("已将已有方案状态设为已通过")
    conn.commit()
    conn.close()
    print("迁移完成")

if __name__ == "__main__":
    migrate()
