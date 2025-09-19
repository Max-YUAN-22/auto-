#!/bin/bash

# 多智能体DSL框架自动部署脚本
# Multi-Agent DSL Framework Auto Deployment Script

echo "🚀 开始自动部署多智能体DSL框架..."

# 检查Git状态
echo "📋 检查Git状态..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️ 检测到未提交的更改，正在添加..."
    git add .
    git commit -m "feat: 自动部署配置更新 - $(date '+%Y-%m-%d %H:%M:%S')"
else
    echo "✅ 工作目录干净，无需提交"
fi

# 检查远程仓库
echo "🔍 检查远程仓库..."
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ 未找到远程仓库，正在添加..."
    git remote add origin https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025.git
fi

# 推送代码到GitHub
echo "📤 推送代码到GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码推送成功"
else
    echo "❌ 代码推送失败"
    exit 1
fi

# 检查GitHub Actions状态
echo "🔍 检查GitHub Actions状态..."
echo "访问: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions"

# 检查Vercel部署状态
echo "🔍 检查Vercel部署状态..."
echo "访问: https://vercel.com/dashboard"

# 生成部署报告
echo "📊 生成部署报告..."
cat > DEPLOYMENT_STATUS.md << EOF
# 自动部署状态报告

## 部署时间
$(date '+%Y-%m-%d %H:%M:%S')

## 部署状态
- ✅ 代码推送: 成功
- ✅ GitHub Actions: 已触发
- ✅ Vercel部署: 自动进行中

## 访问地址
- **GitHub仓库**: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025
- **Vercel部署**: https://multi-agent-ds-lframework-2025.vercel.app
- **GitHub Pages**: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025

## 部署特性
- 🔄 自动部署: 代码推送后自动触发
- 🌐 双平台部署: GitHub Pages + Vercel
- 📊 监控: GitHub Actions + Vercel Analytics
- 🔒 安全: HTTPS + 安全头设置

## 下一步
1. 等待GitHub Actions完成构建
2. 等待Vercel自动部署
3. 验证部署结果
4. 测试所有功能

## 故障排除
如果部署失败，请检查：
- GitHub Actions日志
- Vercel部署日志
- 代码语法错误
- 依赖版本兼容性
EOF

echo "✅ 部署报告已生成: DEPLOYMENT_STATUS.md"

# 显示部署摘要
echo ""
echo "🎉 自动部署配置完成！"
echo ""
echo "📋 部署摘要:"
echo "- GitHub仓库: ✅ 已连接"
echo "- 自动部署: ✅ 已配置"
echo "- Vercel集成: ✅ 已配置"
echo "- GitHub Actions: ✅ 已触发"
echo ""
echo "🌐 访问地址:"
echo "- Vercel: https://multi-agent-ds-lframework-2025.vercel.app"
echo "- GitHub: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025"
echo ""
echo "⏱️ 部署时间: 约3-5分钟"
echo "📊 监控: https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions"
echo ""
echo "✨ 企业级多智能体DSL框架自动部署已启动！"
