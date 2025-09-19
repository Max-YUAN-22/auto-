#!/bin/bash

echo "🔍 Vercel空白页面深度诊断"
echo "=========================="

# 检查部署状态
echo "📡 检查部署状态..."
curl -s -I https://multi-agent-ds-lframework-2025.vercel.app | head -5

echo ""
echo "📄 检查HTML内容..."
HTML_CONTENT=$(curl -s https://multi-agent-ds-lframework-2025.vercel.app)
echo "HTML长度: ${#HTML_CONTENT} 字符"
echo "HTML开头: ${HTML_CONTENT:0:200}..."

echo ""
echo "⚙️ 检查JavaScript文件..."
JS_URL=$(echo "$HTML_CONTENT" | grep -o 'src="[^"]*\.js"' | head -1 | sed 's/src="//' | sed 's/"//')
if [ -n "$JS_URL" ]; then
    echo "JavaScript URL: $JS_URL"
    JS_STATUS=$(curl -s -I "https://multi-agent-ds-lframework-2025.vercel.app$JS_URL" | head -1)
    echo "JavaScript状态: $JS_STATUS"
    JS_SIZE=$(curl -s "https://multi-agent-ds-lframework-2025.vercel.app$JS_URL" | wc -c)
    echo "JavaScript大小: $JS_SIZE bytes"
else
    echo "❌ 未找到JavaScript文件"
fi

echo ""
echo "🎯 检查关键元素..."
if echo "$HTML_CONTENT" | grep -q '<div id="root">'; then
    echo "✅ 找到React根元素"
else
    echo "❌ 未找到React根元素"
fi

if echo "$HTML_CONTENT" | grep -q 'script.*defer'; then
    echo "✅ 找到defer脚本"
else
    echo "❌ 未找到defer脚本"
fi

echo ""
echo "🔧 检查本地构建文件..."
if [ -f "frontend/build/index.html" ]; then
    echo "✅ 本地构建文件存在"
    LOCAL_HTML=$(cat frontend/build/index.html)
    echo "本地HTML长度: ${#LOCAL_HTML} 字符"
    
    # 比较本地和远程HTML
    if [ "$HTML_CONTENT" = "$LOCAL_HTML" ]; then
        echo "✅ 本地和远程HTML内容一致"
    else
        echo "⚠️ 本地和远程HTML内容不一致"
        echo "差异分析:"
        echo "本地: ${LOCAL_HTML:0:100}..."
        echo "远程: ${HTML_CONTENT:0:100}..."
    fi
else
    echo "❌ 本地构建文件不存在"
fi

echo ""
echo "📊 诊断总结:"
echo "============"
if [ ${#HTML_CONTENT} -gt 500 ]; then
    echo "✅ HTML内容正常 (${#HTML_CONTENT} 字符)"
else
    echo "❌ HTML内容异常 (${#HTML_CONTENT} 字符)"
fi

if [ -n "$JS_URL" ] && [ "$JS_SIZE" -gt 100000 ]; then
    echo "✅ JavaScript文件正常 ($JS_SIZE bytes)"
else
    echo "❌ JavaScript文件异常"
fi

echo ""
echo "🎯 可能的问题:"
echo "1. JavaScript执行错误"
echo "2. React组件渲染失败"
echo "3. 资源加载问题"
echo "4. 浏览器兼容性问题"
echo ""
echo "🔧 建议解决方案:"
echo "1. 检查浏览器控制台错误"
echo "2. 访问调试页面: https://multi-agent-ds-lframework-2025.vercel.app/debug.html"
echo "3. 清除浏览器缓存"
echo "4. 尝试不同浏览器"
