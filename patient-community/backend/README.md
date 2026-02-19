# 患者社区后端

基于FastAPI的患者社区后端服务。

## 功能特性

- 用户认证（注册、登录、JWT）
- 病历管理（上传、查看、删除）
- AI智能提取病历信息
- 患者相似度匹配
- 社区交流（发帖、评论、点赞）
- 治疗方案库

## 技术栈

- FastAPI - Web框架
- SQLAlchemy - ORM
- MySQL - 数据库
- JWT - 认证
- OpenAI API - AI信息提取

## 安装依赖

```bash
pip install -r requirements.txt
```

## 数据库配置

1. 创建MySQL数据库：
```sql
CREATE DATABASE patient_community CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `app/config.py` 中的数据库连接字符串

3. 初始化数据库：
```bash
python init_db.py
```

## 运行

开发模式：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

生产模式：
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 环境变量

创建 `.env` 文件：
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/patient_community
SECRET_KEY=your_secret_key
```

## 测试账号

- 用户名: testuser
- 密码: 123456
