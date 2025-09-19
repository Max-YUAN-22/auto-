# 🚀 一键部署多智能体DSL框架
# One-Click Deployment Guide for Multi-Agent DSL Framework

## 📋 部署方案概览

我们提供了多种部署方案，让用户无需自行部署即可使用：

### 🌐 方案一：Vercel + Railway (推荐)
- **前端**: Vercel (免费，全球CDN)
- **后端**: Railway (免费额度，自动部署)
- **优势**: 完全免费，自动部署，全球访问

### 🔧 方案二：GitHub Pages + Heroku
- **前端**: GitHub Pages (免费)
- **后端**: Heroku (免费额度)
- **优势**: 使用GitHub生态，易于管理

## 🎯 快速部署步骤

### 1. 准备仓库
```bash
# 克隆项目
git clone https://github.com/Max-YUAN-22/Final-DSL.git
cd Final-DSL

# 推送到您的GitHub仓库
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. 部署后端 (Railway)

1. 访问 [Railway.app](https://railway.app)
2. 使用GitHub账号登录
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择您的仓库
5. Railway会自动检测到Python项目并部署
6. 部署完成后，复制生成的URL (如: `https://multi-agent-dsl-backend.railway.app`)

### 3. 部署前端 (Vercel)

1. 访问 [Vercel.com](https://vercel.com)
2. 使用GitHub账号登录
3. 点击 "New Project" → "Import Git Repository"
4. 选择您的仓库
5. 在环境变量中添加：
   ```
   REACT_APP_BACKEND_URL = https://your-backend-url.railway.app
   ```
6. 点击 "Deploy"

### 4. 更新前端配置

部署完成后，更新 `vercel.json` 中的后端URL：
```json
{
  "env": {
    "REACT_APP_BACKEND_URL": "https://your-actual-backend-url.railway.app"
  }
}
```

## 🔧 手动部署 (备选方案)

### 使用GitHub Actions自动部署

项目已包含 `.github/workflows/deploy.yml` 文件，支持：

1. **自动构建**: 推送代码时自动构建
2. **自动部署**: 构建成功后自动部署到GitHub Pages
3. **后端部署**: 自动部署到Heroku (需要配置API密钥)

### 配置GitHub Actions

1. 在GitHub仓库设置中添加Secrets：
   - `HEROKU_API_KEY`: Heroku API密钥
   - `HEROKU_EMAIL`: Heroku账号邮箱

2. 推送代码到main分支，GitHub Actions会自动执行部署

## 🌍 访问部署的应用

部署完成后，用户可以通过以下方式访问：

### 直接访问
- **前端地址**: `https://your-app.vercel.app`
- **后端API**: `https://your-backend.railway.app`

### 功能验证
1. **智能体交互**: 访问首页，测试各种智能体任务
2. **企业仪表板**: 查看系统监控和性能指标
3. **系统设置**: 配置API密钥，验证服务连接

## 📱 移动端支持

部署的应用完全支持移动端访问：
- 响应式设计
- 触摸友好的界面
- 移动端优化的导航

## 🔒 安全配置

### 生产环境安全
1. **HTTPS**: 所有部署平台默认支持HTTPS
2. **CORS**: 后端已配置跨域安全
3. **API密钥**: 通过环境变量安全管理

### 环境变量配置
```bash
# 后端环境变量 (Railway/Heroku)
DEEPSEEK_API_KEY=your_deepseek_key
OPENAI_API_KEY=your_openai_key
OPENWEATHER_API_KEY=your_openweather_key

# 前端环境变量 (Vercel)
REACT_APP_BACKEND_URL=https://your-backend-url.railway.app
```

## 🚀 性能优化

### 前端优化
- **代码分割**: React自动代码分割
- **静态资源**: Vercel全球CDN加速
- **缓存策略**: 自动缓存静态资源

### 后端优化
- **自动扩缩**: Railway根据负载自动调整
- **健康检查**: 自动健康检查和重启
- **日志监控**: 实时日志和错误监控

## 📊 监控和维护

### 应用监控
1. **Vercel Analytics**: 前端性能监控
2. **Railway Metrics**: 后端性能监控
3. **GitHub Actions**: 部署状态监控

### 日志查看
- **Vercel**: Dashboard → Functions → Logs
- **Railway**: Project → Deployments → Logs
- **GitHub Actions**: Actions → Workflow runs

## 🔄 更新和维护

### 自动更新
- 推送代码到main分支自动触发部署
- GitHub Actions自动构建和部署
- 无需手动干预

### 手动更新
```bash
# 更新代码
git add .
git commit -m "Update features"
git push origin main

# 部署会自动执行
```

## 🆘 故障排除

### 常见问题

1. **前端无法连接后端**
   - 检查 `REACT_APP_BACKEND_URL` 环境变量
   - 确认后端服务正常运行

2. **API密钥验证失败**
   - 检查API密钥格式
   - 确认API服务可用性

3. **部署失败**
   - 检查GitHub Actions日志
   - 确认环境变量配置正确

### 获取帮助
- 查看部署日志
- 检查GitHub Issues
- 联系技术支持

---

## 🎉 部署完成！

部署成功后，您的多智能体DSL框架将：
- ✅ **全球可访问**: 用户无需安装任何软件
- ✅ **自动更新**: 代码推送自动部署
- ✅ **完全免费**: 使用免费的平台服务
- ✅ **企业级**: 支持API密钥配置和监控

**立即开始使用**: 访问您的部署地址，体验完整的多智能体DSL框架！