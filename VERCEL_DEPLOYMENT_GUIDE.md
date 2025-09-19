# 🚀 Vercel部署指南

## 📋 部署状态

✅ **应用已准备就绪** - 多智能体DSL框架已成功构建，可以部署到 [https://multi-agent-ds-lframework-2025.vercel.app](https://multi-agent-ds-lframework-2025.vercel.app)

## 🎯 部署方式

### 方式1：使用Vercel CLI（推荐）

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 运行部署脚本
./deploy-vercel.sh

# 或者手动部署
cd frontend
vercel --prod
```

### 方式2：通过Vercel网站

1. 访问 [vercel.com](https://vercel.com)
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 导入您的GitHub仓库：`Max-YUAN-22/Multi-Agent_DSLframework-2025`
5. 配置项目设置：
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
6. 点击 "Deploy"

### 方式3：GitHub集成

1. 在Vercel中连接您的GitHub仓库
2. 启用自动部署
3. 每次推送到main分支时自动部署

## 🔧 配置说明

### vercel.json配置
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### package.json配置
- ✅ `homepage: "."` - 支持相对路径
- ✅ 所有必要依赖已安装
- ✅ 构建脚本已配置

## 🎨 应用功能

部署后的应用包含：

1. **🏠 首页** - 项目介绍和性能指标
2. **💻 DSL演示** - 三个核心算法的交互式演示
3. **🤖 智能体管理** - 12个智能体的管理界面
4. **📊 交互记录** - 智能体间协作历史
5. **📚 学术论文** - 研究成果展示
6. **📈 企业仪表板** - 实时系统监控

## 🔗 访问地址

- **Vercel**: https://multi-agent-ds-lframework-2025.vercel.app
- **GitHub Pages**: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/

## ✨ 特性

- 🎨 现代化Material-UI设计
- 📱 响应式移动端支持
- ⚡ 快速加载和渲染
- 🔄 实时数据更新
- 🌐 多语言支持（中文）

## 🆘 故障排除

### 常见问题

1. **构建失败**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm run build
   ```

2. **部署失败**
   - 检查vercel.json配置
   - 确认package.json中的依赖
   - 查看Vercel部署日志

3. **页面空白**
   - 检查浏览器控制台错误
   - 确认静态资源路径正确
   - 验证路由配置

## 🎉 部署完成！

部署成功后，您的多智能体DSL框架将可以通过以下地址访问：
**https://multi-agent-ds-lframework-2025.vercel.app**

享受您的企业级多智能体DSL框架！🚀
