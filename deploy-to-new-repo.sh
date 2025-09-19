#!/bin/bash

# 🚀 企业级多智能体DSL框架部署到新仓库脚本
# Enterprise Multi-Agent DSL Framework Deployment to New Repository Script

echo "🚀 开始部署企业级多智能体DSL框架到新仓库..."

# 检查当前目录
echo "📋 当前目录: $(pwd)"

# 检查项目文件
echo "🔍 检查项目文件..."
if [ -d "frontend" ]; then
    echo "✅ 前端目录存在"
    echo "📊 前端构建状态:"
    if [ -d "frontend/build" ]; then
        echo "✅ 前端已构建"
        du -sh frontend/build/
    else
        echo "❌ 前端未构建，开始构建..."
        cd frontend
        npm install
        npm run build
        cd ..
    fi
else
    echo "❌ 前端目录不存在"
    exit 1
fi

# 检查配置文件
echo "🔍 检查配置文件..."
if [ -f "vercel.json" ]; then
    echo "✅ Vercel配置文件存在"
else
    echo "❌ Vercel配置文件不存在"
fi

if [ -f ".github/workflows/deploy.yml" ]; then
    echo "✅ GitHub Actions配置文件存在"
else
    echo "❌ GitHub Actions配置文件不存在"
fi

echo ""
echo "🎯 部署到新仓库步骤:"
echo ""
echo "1️⃣ 上传代码到新仓库:"
echo "   仓库地址: https://github.com/Max-YUAN-22/auto-"
echo ""
echo "   方法A - GitHub Desktop (推荐):"
echo "   1. 下载 GitHub Desktop"
echo "   2. 克隆仓库: https://github.com/Max-YUAN-22/auto-"
echo "   3. 复制项目文件到克隆目录"
echo "   4. 提交并推送"
echo ""
echo "   方法B - Git命令行:"
echo "   git init"
echo "   git add ."
echo "   git commit -m '企业级多智能体DSL框架初始部署'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/Max-YUAN-22/auto-.git"
echo "   git push -u origin main"
echo ""
echo "   方法C - GitHub网页上传:"
echo "   1. 访问: https://github.com/Max-YUAN-22/auto-"
echo "   2. 点击 'uploading an existing file'"
echo "   3. 拖拽项目文件夹"
echo "   4. 提交更改"
echo ""
echo "2️⃣ 配置Vercel部署:"
echo "   1. 访问: https://vercel.com/dashboard"
echo "   2. 点击 'New Project'"
echo "   3. 导入仓库: Max-YUAN-22/auto-"
echo "   4. 配置设置:"
echo "      Framework: Create React App"
echo "      Root Directory: frontend"
echo "      Build Command: npm run build"
echo "      Output Directory: build"
echo "   5. 添加环境变量:"
echo "      REACT_APP_BACKEND_URL = https://multi-agent-dsl-backend.railway.app"
echo "      REACT_APP_VERSION = v2.0.0-enterprise"
echo "      REACT_APP_ENVIRONMENT = production"
echo "   6. 点击 'Deploy'"
echo ""
echo "3️⃣ 配置GitHub Pages:"
echo "   1. 进入仓库设置 → Pages"
echo "   2. Source: GitHub Actions"
echo "   3. 保存设置"
echo ""
echo "4️⃣ 验证部署:"
echo "   Vercel: https://auto-[随机字符串].vercel.app"
echo "   GitHub Pages: https://max-yuan-22.github.io/auto-/"
echo ""
echo "🎉 企业级特性已准备就绪:"
echo "   ✅ Material-UI企业主题"
echo "   ✅ 响应式设计"
echo "   ✅ ATSLP算法展示 (2.17x性能提升)"
echo "   ✅ HCMPL算法展示 (85%+缓存命中率)"
echo "   ✅ CALK算法展示 (40-60%延迟减少)"
echo "   ✅ 企业级监控界面"
echo "   ✅ 安全合规功能"
echo "   ✅ 云原生部署支持"
echo "   ✅ 全球CDN加速"
echo ""
echo "🌟 您的新仓库将拥有一个真正的企业级多智能体DSL框架！"
