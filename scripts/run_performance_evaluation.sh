#!/bin/bash

# Multi-Agent DSL Framework Performance Testing Script
# 多智能体DSL框架性能测试脚本

echo "🚀 Starting Multi-Agent DSL Framework Performance Evaluation"
echo "============================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking required packages..."
python3 -c "
import asyncio
import matplotlib
import pandas
import numpy
import psutil
print('✅ All required packages are available')
" 2>/dev/null || {
    echo "❌ Missing required packages. Installing..."
    pip3 install matplotlib pandas numpy psutil asyncio
}

# Create results directory
mkdir -p results/performance
mkdir -p docs

echo "📊 Running comprehensive performance evaluation..."
echo "This may take several minutes..."

# Run the performance evaluation
python3 scripts/comprehensive_performance_evaluation.py

if [ $? -eq 0 ]; then
    echo "✅ Performance evaluation completed successfully!"
    echo ""
    echo "📁 Results saved to:"
    echo "   - results/performance/evaluation_report.md"
    echo "   - results/performance/evaluation_results.json"
    echo "   - results/performance/*.png (visualization plots)"
    echo ""
    echo "📖 Theoretical foundation document:"
    echo "   - docs/theoretical_foundation.md"
    echo ""
    echo "🎯 Key findings:"
    echo "   - Scalability analysis with up to 100 agents"
    echo "   - Baseline framework comparison"
    echo "   - Cache performance analysis"
    echo "   - Latency analysis for different task complexities"
    echo ""
    echo "📈 Generated visualizations:"
    echo "   - Scalability analysis plots"
    echo "   - Framework comparison charts"
    echo "   - Cache performance graphs"
    echo "   - Latency distribution plots"
else
    echo "❌ Performance evaluation failed!"
    exit 1
fi

echo ""
echo "🎉 Performance evaluation and theoretical analysis completed!"
echo "The system is now ready for academic publication with comprehensive"
echo "experimental results and theoretical foundations."
