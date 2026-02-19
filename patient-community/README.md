# 患者社区 - 中国版PatientsLikeMe

一个帮助患者找到相似病情的人、分享治疗经验、获得最佳解决方案的患者社区平台。

## 项目简介

本项目是参考PatientsLikeMe打造的中国版患者社区平台，旨在为患者提供：

- **病历管理**：便捷上传病历，AI智能提取关键信息
- **患者匹配**：基于病历信息匹配相似患者和治疗方案
- **社区交流**：加入疾病社区，与病友分享经验和支持
- **治疗方案库**：查看最佳治疗方案和真实效果反馈

## 技术栈

### 前端
- Vue 3 - 渐进式JavaScript框架
- Vite - 下一代前端构建工具
- Element Plus - Vue 3 UI组件库
- Pinia - Vue状态管理
- Vue Router - 路由管理
- Axios - HTTP客户端

### 后端
- FastAPI - 现代Python Web框架
- SQLAlchemy - Python ORM
- MySQL - 关系型数据库
- JWT - 身份认证
- OpenAI API - AI信息提取

## 核心功能

### 1. 用户认证
- 用户注册（支持用户名、邮箱、手机号）
- 用户登录
- JWT Token认证
- 个人信息管理

### 2. 病历管理
- 支持上传图片、PDF等格式的病历文件
- AI自动提取病历关键信息（疾病名称、症状、治疗方案等）
- 病历列表查看和管理
- 病历删除

### 3. 智能匹配
- 基于病历信息的患者相似度计算
- 推荐相似患者列表
- 相似度评分展示
- 推荐治疗方案

### 4. 社区交流
- 多个疾病社区分类
- 发布帖子和评论
- 点赞和互动
- 社区成员统计

### 5. 治疗方案库
- 分类展示治疗方案
- 方案详情和效果反馈
- 成功率和使用人数统计
- 方案搜索功能

## 项目结构

```
patient-community/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/             # API接口
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理
│   │   ├── utils/           # 工具函数
│   │   ├── views/           # 页面组件
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── api/             # API路由
│   │   ├── models/          # 数据模型
│   │   ├── schemas/         # Pydantic模型
│   │   ├── services/        # 业务逻辑
│   │   ├── utils/           # 工具函数
│   │   ├── config.py        # 配置文件
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # 应用入口
│   ├── uploads/             # 上传文件目录
│   ├── init_db.py           # 数据库初始化
│   └── requirements.txt     # Python依赖
│
└── README.md                # 项目说明
```

## 快速开始

### 前置要求

- Node.js 18+
- Python 3.11+
- MySQL 8.0+
- OpenAI API Key

### 1. 克隆项目

```bash
cd /home/ubuntu/patient-community
```

### 2. 配置数据库

创建MySQL数据库：

```sql
CREATE DATABASE patient_community CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 后端设置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
# 创建 .env 文件并配置：
# OPENAI_API_KEY=your_openai_api_key
# DATABASE_URL=mysql+pymysql://user:password@localhost:3306/patient_community
# SECRET_KEY=your_secret_key

# 初始化数据库
python init_db.py

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端API文档：http://localhost:8000/docs

### 4. 前端设置

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

前端访问地址：http://localhost:3000

## 默认测试账号

- 用户名: testuser
- 密码: 123456

## API接口

### 认证相关
- POST `/api/auth/register` - 用户注册
- POST `/api/auth/login` - 用户登录
- GET `/api/auth/profile` - 获取用户信息
- PUT `/api/auth/profile` - 更新用户信息

### 病历管理
- POST `/api/records/upload` - 上传病历
- GET `/api/records` - 获取病历列表
- GET `/api/records/{id}` - 获取病历详情
- DELETE `/api/records/{id}` - 删除病历
- POST `/api/records/{id}/process` - AI处理病历

### 患者匹配
- GET `/api/match/similar` - 获取相似患者
- GET `/api/match/recommendations` - 获取推荐方案

### 社区
- GET `/api/communities` - 获取社区列表
- GET `/api/communities/{id}/posts` - 获取社区帖子
- POST `/api/posts` - 发布帖子
- POST `/api/posts/{id}/comments` - 发表评论
- POST `/api/posts/{id}/like` - 点赞

## 数据库设计

### 主要数据表

- `users` - 用户表
- `medical_records` - 病历表
- `medical_info` - 病历信息表
- `communities` - 社区表
- `posts` - 帖子表
- `comments` - 评论表
- `treatment_solutions` - 治疗方案表

详细的数据库设计请参考 `/home/ubuntu/system_design.md`

## 功能特色

### AI智能提取
使用OpenAI API从病历文件中自动提取：
- 疾病名称
- 症状描述
- 诊断日期
- 治疗方案
- 用药情况

### 相似度匹配算法
基于多维度计算患者相似度：
- 疾病类型匹配（权重40%）
- 症状相似度（权重30%）
- 治疗方案相似度（权重30%）

### 响应式设计
- 支持桌面端和移动端
- 现代化的UI设计
- 流畅的用户体验

## 开发说明

### 前端开发

```bash
cd frontend

# 开发模式
pnpm dev

# 构建生产版本
pnpm build

# 预览生产版本
pnpm preview
```

### 后端开发

```bash
cd backend

# 开发模式（自动重载）
uvicorn app.main:app --reload

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 部署建议

### 前端部署
- 使用Nginx托管静态文件
- 配置反向代理到后端API

### 后端部署
- 使用Gunicorn + Uvicorn workers
- 配置Nginx反向代理
- 使用systemd管理服务

### 数据库
- 使用MySQL 8.0+
- 配置定期备份
- 优化索引和查询

## 注意事项

1. **OpenAI API Key**: 需要配置有效的OpenAI API Key才能使用AI提取功能
2. **数据库配置**: 请根据实际情况修改数据库连接字符串
3. **安全性**: 生产环境请修改SECRET_KEY和其他敏感配置
4. **文件上传**: 默认上传限制为10MB，可根据需要调整

## 后续优化方向

- [ ] 实现实时聊天功能
- [ ] 添加数据可视化分析
- [ ] 支持更多文件格式
- [ ] 优化AI提取准确率
- [ ] 添加移动端App
- [ ] 实现推送通知
- [ ] 添加用户隐私保护
- [ ] 完善社区管理功能

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提Issue或PR。
