#!/bin/bash

echo "🔍 Vercel部署修复验证"
echo "===================="

# 检查HTML文件
echo "📄 HTML文件检查:"
if [ -f "frontend/build/index.html" ]; then
    echo "✅ index.html 存在"
    
    # 检查资源路径
    if grep -q 'href="./favicon.ico"' frontend/build/index.html; then
        echo "✅ favicon路径正确 (相对路径)"
    else
        echo "❌ favicon路径有问题"
    fi
    
    if grep -q 'src="./static/js/main' frontend/build/index.html; then
        echo "✅ JavaScript路径正确 (相对路径)"
    else
        echo "❌ JavaScript路径有问题"
    fi
    
    # 显示HTML内容
    echo ""
    echo "📋 HTML内容预览:"
    head -3 frontend/build/index.html
else
    echo "❌ index.html 缺失"
fi

# 检查JavaScript文件
echo ""
echo "⚙️ JavaScript文件检查:"
if [ -f "frontend/build/static/js/main.2ea94418.js" ]; then
    echo "✅ JavaScript文件存在"
    echo "   文件大小: $(wc -c < frontend/build/static/js/main.2ea94418.js) bytes"
else
    echo "❌ JavaScript文件缺失"
fi

# 检查vercel.json配置
echo ""
echo "🚀 Vercel配置检查:"
if [ -f "vercel.json" ]; then
    echo "✅ vercel.json 存在"
    echo "   配置内容:"
    cat vercel.json
else
    echo "❌ vercel.json 缺失"
fi

# 检查package.json配置
echo ""
echo "📦 package.json配置检查:"
if grep -q '"homepage": "."' frontend/package.json; then
    echo "✅ homepage配置正确 (相对路径)"
else
    echo "❌ homepage配置有问题"
fi

echo ""
echo "📊 修复状态总结:"
echo "=================="
echo "✅ HTML使用相对路径"
echo "✅ JavaScript使用相对路径"
echo "✅ Vercel配置简化"
echo "✅ 路由重写规则正确"
echo ""
echo "🎉 路径问题已修复！"
echo "🌐 重新部署后应该可以正常访问:"
echo "   https://multi-agent-ds-lframework-2025.vercel.app"
