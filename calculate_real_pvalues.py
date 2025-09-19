#!/usr/bin/env python3
"""
计算真实的p-value - 基于实际数据进行t检验
"""

import json
import numpy as np
from scipy.stats import ttest_ind
from typing import Dict, List, Tuple

def load_real_data():
    """加载真实数据"""
    try:
        with open('data/statistical_analysis_results.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['stats']
    except FileNotFoundError:
        print("❌ 未找到统计测试数据文件")
        return None

def calculate_real_pvalues(stats: Dict[str, any]) -> Dict[str, float]:
    """计算真实的p-value"""
    print("🧪 计算真实的p-value")
    
    our_dsl_data = np.array(stats['Our DSL']['data'])
    pvalues = {}
    
    frameworks = ['LangChain', 'CrewAI', 'AutoGen']
    
    for framework in frameworks:
        other_data = np.array(stats[framework]['data'])
        
        # 进行独立样本t检验
        # H0: Our DSL和framework的内存使用无显著差异
        # H1: Our DSL的内存使用显著低于framework
        
        t_stat, p_value = ttest_ind(our_dsl_data, other_data, alternative='less')
        
        pvalues[framework] = p_value
        
        print(f"{framework} vs Our DSL:")
        print(f"  t-statistic: {t_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        print(f"  显著性: {'显著' if p_value < 0.05 else '不显著'}")
        print()
    
    return pvalues

def format_pvalue(p_value: float) -> str:
    """格式化p-value显示"""
    if p_value < 0.001:
        return "<0.001"
    elif p_value < 0.01:
        return f"{p_value:.3f}"
    elif p_value < 0.05:
        return f"{p_value:.3f}"
    else:
        return f"{p_value:.3f}"

def main():
    """主函数"""
    print("🔬 计算真实的p-value")
    
    # 加载数据
    stats = load_real_data()
    if not stats:
        return
    
    # 计算p-value
    pvalues = calculate_real_pvalues(stats)
    
    # 格式化结果
    print("📊 格式化后的p-value:")
    for framework, p_value in pvalues.items():
        formatted = format_pvalue(p_value)
        print(f"{framework}: {formatted}")
    
    # 保存结果
    result = {
        'pvalues': pvalues,
        'formatted_pvalues': {fw: format_pvalue(pv) for fw, pv in pvalues.items()}
    }
    
    with open('real_pvalues.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("\n💾 真实p-value结果已保存到 real_pvalues.json")
    
    return pvalues

if __name__ == "__main__":
    main()
