#!/bin/bash

echo "📊 GitHub Actions CI/CD 管道状态监控"
echo "===================================="

echo "⏱️ 等待CI/CD管道启动..."
sleep 10

echo ""
echo "🔍 检查最新工作流运行状态..."

# 获取最新的工作流运行ID
LATEST_RUN=$(curl -s -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions/runs" \
  | jq -r '.workflow_runs[0].id')

if [ "$LATEST_RUN" != "null" ] && [ "$LATEST_RUN" != "" ]; then
    echo "📋 最新工作流运行ID: $LATEST_RUN"
    
    # 获取工作流运行状态
    RUN_STATUS=$(curl -s -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions/runs/$LATEST_RUN" \
      | jq -r '.status')
    
    echo "📊 运行状态: $RUN_STATUS"
    
    if [ "$RUN_STATUS" = "completed" ]; then
        # 获取工作流运行结果
        RUN_CONCLUSION=$(curl -s -H "Accept: application/vnd.github.v3+json" \
          "https://api.github.com/repos/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions/runs/$LATEST_RUN" \
          | jq -r '.conclusion')
        
        echo "🎯 运行结果: $RUN_CONCLUSION"
        
        if [ "$RUN_CONCLUSION" = "success" ]; then
            echo "✅ CI/CD管道运行成功！"
        else
            echo "❌ CI/CD管道运行失败"
        fi
    else
        echo "🔄 CI/CD管道正在运行中..."
    fi
else
    echo "❌ 无法获取工作流运行信息"
fi

echo ""
echo "🌐 访问GitHub Actions页面查看详细状态:"
echo "https://github.com/Max-YUAN-22/Multi-Agent_DSLframework-2025/actions"

echo ""
echo "📱 部署地址:"
echo "• GitHub Pages: https://max-yuan-22.github.io/Multi-Agent_DSLframework-2025/"
echo "• Vercel: https://multi-agent-ds-lframework-2025.vercel.app"

echo ""
echo "🔧 如果仍有问题，请检查:"
echo "1. GitHub Secrets 配置 (VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID)"
echo "2. 仓库权限设置"
echo "3. 工作流文件语法"
