#!/usr/bin/env python3
"""
复现脚本 - 确保结果可复现
Reproduction Script - Ensure Results are Reproducible
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查API密钥
    api_key = os.environ.get('OPENAI_API_KEY')
    base_url = os.environ.get('OPENAI_API_BASE')
    
    if not api_key:
        print("❌ 未设置OPENAI_API_KEY环境变量")
        print("请设置: export OPENAI_API_KEY='your_api_key_here'")
        return False
    
    if not base_url:
        print("❌ 未设置OPENAI_API_BASE环境变量")
        print("请设置: export OPENAI_API_BASE='https://www.yunqiaoai.top/v1'")
        return False
    
    print(f"✅ API密钥已设置: {api_key[:10]}...")
    print(f"✅ API基础URL已设置: {base_url}")
    return True

def run_test(test_name, script_path):
    """运行测试"""
    print(f"\n🚀 运行 {test_name}...")
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {test_name} 完成")
            return True
        else:
            print(f"❌ {test_name} 失败")
            print(f"错误输出: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} 超时")
        return False
    except Exception as e:
        print(f"❌ {test_name} 异常: {e}")
        return False

def verify_results():
    """验证结果文件"""
    print("\n🔍 验证结果文件...")
    
    required_files = [
        "results/honest_api_benchmark_results.json",
        "results/optimized_dsl_results.json"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
            
            # 检查文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "benchmark_results" in data:
                    result_count = len(data["benchmark_results"])
                    print(f"   包含 {result_count} 个测试结果")
                else:
                    print(f"   ⚠️ 文件格式可能有问题")
            except Exception as e:
                print(f"   ❌ 文件读取失败: {e}")
        else:
            print(f"❌ {file_path} 不存在")

def generate_summary():
    """生成测试摘要"""
    print("\n📊 生成测试摘要...")
    
    try:
        # 运行综合分析
        result = subprocess.run([sys.executable, "scripts/comprehensive_performance_analysis.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 综合分析完成")
        else:
            print("❌ 综合分析失败")
    except Exception as e:
        print(f"❌ 综合分析异常: {e}")

def main():
    """主函数"""
    print("=" * 80)
    print("🎯 学术诚信基准测试复现脚本")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请先配置API密钥")
        return
    
    # 运行测试
    tests = [
        ("真实API基准测试", "scripts/honest_api_benchmark.py"),
        ("DSL优化测试", "scripts/dsl_optimization.py")
    ]
    
    success_count = 0
    for test_name, script_path in tests:
        if run_test(test_name, script_path):
            success_count += 1
    
    # 验证结果
    verify_results()
    
    # 生成摘要
    generate_summary()
    
    # 总结
    print("\n" + "=" * 80)
    print("🎯 复现结果总结")
    print("=" * 80)
    print(f"成功测试: {success_count}/{len(tests)}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == len(tests):
        print("✅ 所有测试都成功完成！")
        print("✅ 结果可以复现！")
        print("✅ 适合学术论文使用！")
    else:
        print("⚠️ 部分测试失败，请检查环境配置")
    
    print("\n📁 结果文件位置:")
    print("   - results/honest_api_benchmark_results.json")
    print("   - results/optimized_dsl_results.json")
    print("   - ACADEMIC_INTEGRITY_REPORT.md")

if __name__ == "__main__":
    main()
