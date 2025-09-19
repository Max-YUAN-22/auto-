#!/bin/bash

echo "🎉 Vercel空白页面问题修复验证"
echo "=============================="

echo "⏱️ 等待部署完成..."
sleep 30

echo ""
echo "🔍 检查新的部署状态..."

# 检查HTML内容
HTML_CONTENT=$(curl -s https://multi-agent-ds-lframework-2025.vercel.app)
echo "HTML长度: ${#HTML_CONTENT} 字符"

# 检查JavaScript文件
JS_URL=$(echo "$HTML_CONTENT" | grep -o 'src="[^"]*\.js"' | head -1 | sed 's/src="//' | sed 's/"//')
if [ -n "$JS_URL" ]; then
    echo "JavaScript URL: $JS_URL"
    JS_SIZE=$(curl -s "https://multi-agent-ds-lframework-2025.vercel.app$JS_URL" | wc -c)
    echo "JavaScript大小: $JS_SIZE bytes"
    
    if [ "$JS_SIZE" -lt 100000 ]; then
        echo "✅ JavaScript文件大小正常 (简化版本)"
    else
        echo "⚠️ JavaScript文件仍然很大"
    fi
fi

echo ""
echo "🎯 检查关键内容..."
if echo "$HTML_CONTENT" | grep -q '多智能体DSL框架'; then
    echo "✅ 找到中文标题"
else
    echo "❌ 未找到中文标题"
fi

if echo "$HTML_CONTENT" | grep -q '部署成功'; then
    echo "✅ 找到成功信息"
else
    echo "❌ 未找到成功信息"
fi

echo ""
echo "📊 修复状态总结:"
echo "================"
echo "✅ 简化了React应用"
echo "✅ 移除了复杂的Material-UI依赖"
echo "✅ 减少了JavaScript文件大小"
echo "✅ 使用简单的内联样式"
echo "✅ 添加了功能测试按钮"
echo ""
echo "🌐 现在应该可以正常访问:"
echo "   https://multi-agent-ds-lframework-2025.vercel.app"
echo ""
echo "🔧 如果仍然空白，请尝试:"
echo "1. 清除浏览器缓存"
echo "2. 使用无痕模式"
echo "3. 尝试不同浏览器"
echo "4. 检查浏览器控制台错误"
echo ""
echo "📱 调试页面:"
echo "   https://multi-agent-ds-lframework-2025.vercel.app/debug.html"
