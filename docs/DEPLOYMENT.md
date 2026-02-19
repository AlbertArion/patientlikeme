# 患者社区项目部署说明

## 当前运行状态

### 服务地址
- **前端地址**: https://3000-i9vsk9cwbog8xzwzo460r-0ecdc938.sg1.manus.computer
- **后端API**: https://8000-i9vsk9cwbog8xzwzo460r-0ecdc938.sg1.manus.computer
- **API文档**: https://8000-i9vsk9cwbog8xzwzo460r-0ecdc938.sg1.manus.computer/docs

### 测试账号
- 用户名: `testuser`
- 密码: `123456`

## 项目结构

```
/home/ubuntu/patient-community/
├── frontend/          # Vue 3 + Vite 前端项目
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── api/      # API接口
│   │   ├── stores/   # 状态管理
│   │   └── router/   # 路由配置
│   └── package.json
│
├── backend/           # FastAPI 后端项目
│   ├── app/
│   │   ├── api/      # API路由
│   │   ├── models/   # 数据模型
│   │   ├── services/ # 业务逻辑
│   │   └── main.py   # 应用入口
│   ├── patient_community.db  # SQLite数据库
│   └── requirements.txt
│
└── README.md          # 项目说明
```

## 核心功能

### 1. 用户认证
- ✅ 用户注册（支持用户名、邮箱、手机号）
- ✅ 用户登录（JWT认证）
- ✅ 用户信息管理

### 2. 病历管理
- ✅ 病历上传（支持图片、PDF等格式）
- ✅ 病历列表查看
- ✅ AI智能提取病历信息
- ✅ 病历删除

### 3. 患者匹配
- ✅ 基于病历信息的相似度计算
- ✅ 推荐相似患者
- ✅ 相似度评分展示

### 4. 社区交流
- ✅ 多个疾病社区
- ✅ 发布帖子
- ✅ 评论和点赞
- ✅ 社区成员统计

### 5. 治疗方案库
- ✅ 方案分类展示
- ✅ 方案详情
- ✅ 成功率和使用人数统计
- ✅ 方案搜索

## 技术实现

### 前端技术栈
- **Vue 3**: 渐进式JavaScript框架
- **Vite**: 下一代前端构建工具
- **Element Plus**: Vue 3 UI组件库
- **Pinia**: 状态管理
- **Vue Router**: 路由管理
- **Axios**: HTTP客户端

### 后端技术栈
- **FastAPI**: 现代Python Web框架
- **SQLAlchemy**: Python ORM
- **SQLite**: 轻量级数据库（可切换至MySQL）
- **JWT**: 身份认证
- **OpenAI API**: AI信息提取

### AI功能
使用OpenAI API从病历中提取：
- 疾病名称
- 症状描述
- 诊断日期
- 治疗方案
- 用药情况

### 匹配算法
相似度计算基于：
- 疾病类型匹配（权重40%）
- 症状相似度（权重30%）
- 治疗方案相似度（权重30%）

## 本地开发

### 启动后端
```bash
cd /home/ubuntu/patient-community/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 启动前端
```bash
cd /home/ubuntu/patient-community/frontend
pnpm dev
```

### 初始化数据库
```bash
cd /home/ubuntu/patient-community/backend
python3 init_db.py
```

## 数据库说明

当前使用SQLite数据库（`patient_community.db`），包含以下数据表：

- `users` - 用户表
- `medical_records` - 病历表
- `medical_info` - 病历信息表
- `communities` - 社区表
- `posts` - 帖子表
- `comments` - 评论表
- `treatment_solutions` - 治疗方案表

### 切换到MySQL

如需切换到MySQL，修改 `backend/app/config.py`：

```python
DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/patient_community?charset=utf8mb4"
```

然后创建MySQL数据库：
```sql
CREATE DATABASE patient_community CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## API接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/profile` - 获取用户信息

### 病历管理
- `POST /api/records/upload` - 上传病历
- `GET /api/records` - 获取病历列表
- `GET /api/records/{id}` - 获取病历详情
- `DELETE /api/records/{id}` - 删除病历
- `POST /api/records/{id}/process` - AI处理病历

### 患者匹配
- `GET /api/match/similar` - 获取相似患者
- `GET /api/match/recommendations` - 获取推荐方案

### 社区
- `GET /api/communities` - 获取社区列表
- `GET /api/communities/{id}/posts` - 获取社区帖子
- `POST /api/posts` - 发布帖子
- `POST /api/posts/{id}/comments` - 发表评论
- `POST /api/posts/{id}/like` - 点赞

## 使用流程

1. **注册/登录**
   - 访问首页，点击"立即加入"或"登录"
   - 使用测试账号登录：testuser / 123456

2. **上传病历**
   - 进入"我的病历"页面
   - 点击"上传病历"按钮
   - 选择病历文件（支持图片、PDF）
   - 上传成功后点击"AI提取"按钮

3. **查看相似患者**
   - 等待病历处理完成
   - 进入"相似患者"页面
   - 查看系统推荐的相似患者和相似度

4. **参与社区**
   - 进入"社区"页面
   - 选择相关疾病社区
   - 浏览帖子或发布新帖子
   - 点赞和评论

5. **查看治疗方案**
   - 进入"治疗方案库"页面
   - 搜索或浏览治疗方案
   - 查看方案详情和效果反馈

## 注意事项

1. **OpenAI API Key**: 
   - 当前使用环境变量中的OPENAI_API_KEY
   - AI提取功能需要有效的API Key

2. **文件上传限制**:
   - 最大文件大小：10MB
   - 支持格式：JPG、PNG、PDF、DOC、DOCX

3. **数据库**:
   - 当前使用SQLite，适合开发和测试
   - 生产环境建议使用MySQL

4. **安全性**:
   - 生产环境请修改SECRET_KEY
   - 配置HTTPS
   - 添加速率限制

## 生产部署建议

> 完整步骤、Nginx 配置、服务管理、监控与故障排查见 **[患者社区生产环境部署说明.md](患者社区生产环境部署说明.md)**。

### 前端部署
1. 构建生产版本：
   ```bash
   cd frontend
   pnpm build
   ```

2. 使用Nginx托管静态文件：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           root /path/to/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

### 后端部署
1. 使用Gunicorn + Uvicorn workers：
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. 配置systemd服务：
   ```ini
   [Unit]
   Description=Patient Community API
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/backend
   ExecStart=/usr/local/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

## 后续优化方向

- [ ] 实现实时聊天功能
- [ ] 添加数据可视化分析
- [ ] 支持更多文件格式（DICOM医学影像等）
- [ ] 优化AI提取准确率
- [ ] 添加移动端App
- [ ] 实现推送通知
- [ ] 完善用户隐私保护
- [ ] 添加管理后台

## 技术支持

如有问题，请查看：
- 项目README: `/home/ubuntu/patient-community/README.md`
- 系统设计文档: `/home/ubuntu/system_design.md`
- API文档: https://8000-i9vsk9cwbog8xzwzo460r-0ecdc938.sg1.manus.computer/docs
