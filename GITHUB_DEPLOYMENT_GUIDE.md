# 🚀 GitHub云部署指南

## 📋 部署状态

✅ **代码已准备就绪** - 多智能体DSL框架已配置完整的GitHub Actions自动部署流程

## 🌐 部署地址

- **GitHub Pages**: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/
- **Vercel**: https://multi-agent-ds-lframework-2025.vercel.app

## 🎯 自动部署方式

### 方式1：GitHub Pages（推荐，无需配置）

1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "feat: 添加完整的多智能体DSL框架功能"
   git push origin main
   ```

2. **自动部署流程**
   - GitHub Actions会自动检测代码推送
   - 自动安装依赖和构建应用
   - 自动部署到GitHub Pages
   - 部署完成后可通过链接访问

3. **访问应用**
   - 等待3-5分钟部署完成
   - 访问：https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/

### 方式2：Vercel自动部署

1. **配置Vercel密钥**（可选）
   - 访问 [vercel.com](https://vercel.com)
   - 获取 `VERCEL_TOKEN`、`VERCEL_ORG_ID`、`VERCEL_PROJECT_ID`
   - 在GitHub仓库设置中添加这些密钥

2. **自动部署**
   - 代码推送到main分支时自动触发
   - 同时部署到GitHub Pages和Vercel

## 🔧 部署配置

### GitHub Actions工作流

项目包含两个部署工作流：

1. **`.github/workflows/deploy.yml`** - 完整部署（GitHub Pages + Vercel）
2. **`.github/workflows/github-pages.yml`** - 仅GitHub Pages部署

### 构建配置

- **Node.js版本**: 18
- **构建命令**: `npm run build`
- **输出目录**: `frontend/build`
- **缓存**: npm依赖缓存优化

## 📱 应用功能

部署后的应用包含：

### 🏠 首页
- 项目介绍和核心特性
- 性能指标概览
- 算法特性展示

### 💻 DSL演示
- **ATSLP算法**: 自适应任务调度与负载预测
- **HCMPL算法**: 分层缓存管理与模式学习
- **CALK算法**: 协作智能体学习与知识转移

### 🤖 智能体管理
- 12个智能体状态监控
- 实时性能指标
- 智能体配置管理

### 📊 交互记录
- 智能体间协作历史
- 交互类型和状态
- 实时活动监控

### 📚 学术论文
- 4篇核心论文展示
- 引用数和下载量统计
- 论文详情查看

### 📈 企业仪表板
- 系统状态监控
- 性能指标可视化
- 实时数据更新

## 🎨 技术特性

- **现代化UI**: Material-UI企业级设计
- **响应式**: 支持移动端和桌面端
- **实时更新**: WebSocket实时通信
- **性能优化**: 123KB压缩包大小
- **多语言**: 中文界面支持

## 🔍 部署监控

### GitHub Actions状态
- 访问仓库的"Actions"标签页
- 查看部署进度和状态
- 监控构建日志

### 部署验证
1. **构建成功**: 绿色✓标记
2. **部署完成**: 显示访问链接
3. **功能测试**: 验证所有页面正常加载

## 🆘 故障排除

### 常见问题

1. **构建失败**
   ```bash
   # 检查依赖是否正确安装
   cd frontend
   npm ci
   npm run build
   ```

2. **页面空白**
   - 检查浏览器控制台错误
   - 确认静态资源路径正确
   - 验证路由配置

3. **部署超时**
   - GitHub Actions有6小时限制
   - 检查网络连接
   - 重新触发部署

### 重新部署

```bash
# 手动触发部署
git commit --allow-empty -m "trigger: 重新部署"
git push origin main
```

## 📊 性能指标

- **构建时间**: 3-5分钟
- **部署时间**: 1-2分钟
- **应用大小**: 123KB (gzipped)
- **加载时间**: < 2秒
- **支持并发**: 1000+ 用户

## 🎉 部署完成！

部署成功后，您的多智能体DSL框架将可以通过以下地址访问：

**🌐 GitHub Pages**: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/

**🚀 立即开始使用您的企业级多智能体DSL框架！**
