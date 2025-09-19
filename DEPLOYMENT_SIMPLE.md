# 🤖 多智能体DSL框架
# Multi-Agent DSL Framework

## 🚀 快速部署指南

### 方案一：Vercel + Render（推荐）

#### 1. 部署前端到Vercel
1. 访问 [Vercel.com](https://vercel.com)
2. 导入仓库：`Max-YUAN-22/Multi-Agent_DSLframework-2025`
3. 配置：
   - Framework Preset: Create React App
   - Root Directory: frontend
   - Build Command: npm run build
   - Output Directory: build

#### 2. 部署后端到Render
1. 访问 [Render.com](https://render.com)
2. 创建Web Service
3. 连接仓库：`Max-YUAN-22/Multi-Agent_DSLframework-2025`
4. 配置：
   - Build Command: `pip install -r requirements-render.txt`
   - Start Command: `python render_main.py`

#### 3. 更新环境变量
在Vercel中添加：
```
REACT_APP_BACKEND_URL = https://your-backend-url.onrender.com
```

### 方案二：Railway（备选）

#### 1. 部署后端到Railway
1. 访问 [Railway.app](https://railway.app)
2. 导入仓库
3. Railway会自动检测Python项目

#### 2. 更新Vercel环境变量
```
REACT_APP_BACKEND_URL = https://your-backend-url.railway.app
```

## 📱 本地运行

### 前端
```bash
cd frontend
npm install
npm start
```

### 后端
```bash
pip install -r requirements.txt
python -m backend.main
```

## 🔧 故障排除

### 常见问题
1. **前端无法连接后端**: 检查环境变量
2. **后端部署失败**: 使用简化版本
3. **依赖问题**: 使用requirements-render.txt

### 获取帮助
- 查看部署日志
- 检查环境变量配置
- 参考项目文档

---

**部署成功后，您将拥有一个完整的企业级多智能体DSL框架！** 🎉
