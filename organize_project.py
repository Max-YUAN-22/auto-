#!/usr/bin/env python3
"""
项目文件夹整理脚本
重新组织multi-agent-dsl-final项目的文件结构
"""

import os
import shutil
import glob
from pathlib import Path

def create_directory_structure():
    """创建清晰的目录结构"""
    
    # 定义新的目录结构
    directories = {
        # 核心文档
        'docs/': [
            'ACADEMIC_INTEGRITY_REPORT.md',
            'ACADEMIC_INTEGRITY_STATEMENT.md', 
            'ARCHITECTURE_RESTORE_REPORT.md',
            'COMPREHENSIVE_ACADEMIC_INTEGRITY_REPORT.md',
            'COMPREHENSIVE_PAPER_REVIEW_REPORT.md',
            'FAIRNESS_ANALYSIS_REPORT.md',
            'FINAL_MATHEMATICAL_VERIFICATION_REPORT.md',
            'TRUTHFULNESS_AUDIT_REPORT.md',
            'REPRODUCIBILITY_GUIDE.md',
            'REPRODUCIBILITY_REPORT.md'
        ],
        
        # 论文相关
        'papers/': [
            'CCF_A_CLASS_PAPER.md',
            'CCF_A_CLASS_PAPER_COMPLETE_FINAL.tex',
            'CCF_A_CLASS_PAPER_FINAL.tex', 
            'CCF_A_CLASS_PAPER_HONEST.tex',
            'REAL_WORLD_PAPER_FINAL.tex',
            'CCF_A_CLASS_USAGE_GUIDE.md',
            'PAPER_DATA_UPDATE_DOCUMENTATION.md',
            'PAPER_LENGTH_REPORT.md',
            'PAPER_SUPPLEMENTARY_MATERIALS.md'
        ],
        
        # 指南和说明
        'guides/': [
            'COMPLETE_FINAL_GUIDE.md',
            'DEMO_GUIDE.md',
            'DEPLOYMENT.md',
            'WEB_README.md',
            'FIGURE_TITLES_COMPLETION_REPORT.md',
            'FINAL_CLEAN_TITLES_COMPLETION_REPORT.md',
            'FORMAL_TITLES_COMPLETION_REPORT.md',
            'FINAL_TITLES_COMPLETION_REPORT.md',
            'HONEST_IMAGE_GUIDE.md',
            'IMAGE_RENAME_GUIDE.md',
            'MERMAID_USAGE_GUIDE.md',
            'figure_usage_guide.md'
        ],
        
        # 修复报告
        'reports/fixes/': [
            'FINAL_FIX_REPORT.md',
            'FIXES_REPORT.md',
            'HELP_PANEL_FIX_REPORT.md',
            'INTERACTION_HISTORY_FIX_REPORT.md',
            'LAYOUT_NAVIGATION_FIX_REPORT.md',
            'PAYLOAD_INCLUDES_FIX_REPORT.md',
            'SEND_NAVIGATION_FIX_REPORT.md',
            'SYNTAX_FIX_REPORT.md',
            'FINAL_RESTORE_REPORT.md',
            'RESTORE_ORIGINAL_REPORT.md',
            'FINAL_MERMAID_CLEANUP_REPORT.md',
            'FINAL_TRUTHFULNESS_CORRECTION_REPORT.md',
            'FINAL_WEB_INTEGRATION_REPORT.md',
            'FINAL_CITATION_UPDATE_REPORT.md',
            'FINAL_PAPER_CHECKLIST.md',
            'FINAL_RESTORE_REPORT.md'
        ],
        
        # 提交相关
        'submission/': [
            'SUBMISSION_CHECKLIST.md',
            'SUPERVISOR_SUBMISSION_CHECKLIST.md',
            'SUBMISSION_PACKAGE_README.md'
        ],
        
        # 图表生成脚本
        'scripts/figure_generation/': [
            'generate_ccf_a_charts.py',
            'generate_figures.py',
            'generate_honest_figures.py',
            'generate_latest_figures.py',
            'generate_professional_figures.py',
            'generate_simple_figures.py'
        ],
        
        # 测试和分析脚本
        'scripts/analysis/': [
            'academic_integrity_checker.py',
            'analyze_performance.py',
            'comprehensive_paper_review.py',
            'statistical_validation.py',
            'verify_academic_results.py',
            'quick_validation.py',
            'mini_memory_test.py',
            'quick_memory_test.py',
            'simple_memory_test.py',
            'fix_memory_data.py',
            'update_memory_data.py',
            'reproduce_results.py'
        ],
        
        # 测试脚本
        'scripts/testing/': [
            'test_api.py',
            'test_interaction_flow.py',
            'test_memory_fix.py',
            'test_real_api_integration.py',
            'test_real_interaction.py',
            'test_system.py',
            'test_traffic_realistic.py',
            'test_websocket.py'
        ],
        
        # 数据文件
        'data/': [
            'statistical_analysis_results.json',
            'events.csv',
            'correct_events.csv',
            'test_events.csv',
            'traffic_incident_event.csv'
        ],
        
        # 配置文件
        'config/': [
            'Dockerfile',
            'docker-compose.yml',
            'docker-compose.distributed.yml',
            'nginx.conf',
            'prometheus.yml',
            'requirements.txt',
            'package.json',
            'package-lock.json',
            'env.template',
            'free_api_config.template',
            '.env',
            '.env.example',
            '.envTAB',
            '.gitignore'
        ],
        
        # 启动脚本
        'scripts/startup/': [
            'start_improved.sh',
            'start_simple.sh', 
            'start_system.sh',
            'run_tests.sh'
        ],
        
        # 其他文件
        'misc/': [
            'cli.py',
            'mermaid_diagrams.md',
            'virtual-demo.css',
            'virtual-demo.html',
            'index.html',
            'main.css',
            'LICENSE',
            'README.md'
        ]
    }
    
    return directories

def organize_files():
    """整理文件到新的目录结构"""
    
    directories = create_directory_structure()
    
    print("🗂️ 开始整理项目文件夹...")
    print("=" * 60)
    
    # 创建所有目录
    for dir_path in directories.keys():
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 创建目录: {dir_path}")
    
    # 移动文件到对应目录
    moved_count = 0
    for dir_path, files in directories.items():
        for file_name in files:
            if os.path.exists(file_name):
                dest_path = os.path.join(dir_path, file_name)
                shutil.move(file_name, dest_path)
                print(f"📄 移动: {file_name} -> {dest_path}")
                moved_count += 1
            else:
                print(f"⚠️  文件不存在: {file_name}")
    
    print(f"\n✅ 成功移动 {moved_count} 个文件")
    
    # 处理特殊目录
    handle_special_directories()
    
    print("\n" + "=" * 60)
    print("🎉 文件夹整理完成！")

def handle_special_directories():
    """处理特殊目录的整理"""
    
    # 整理图表目录
    print("\n📊 整理图表目录...")
    
    # 将paper_figures_final移动到figures/目录下
    if os.path.exists('paper_figures_final'):
        if not os.path.exists('figures/final'):
            os.makedirs('figures/final', exist_ok=True)
        
        # 移动paper_figures_final的内容到figures/final
        for item in os.listdir('paper_figures_final'):
            src = os.path.join('paper_figures_final', item)
            dst = os.path.join('figures/final', item)
            if os.path.isfile(src):
                shutil.move(src, dst)
                print(f"📊 移动图表: {item}")
        
        # 删除空的paper_figures_final目录
        os.rmdir('paper_figures_final')
    
    # 整理压缩包
    if os.path.exists('paper_figures_final.zip'):
        shutil.move('paper_figures_final.zip', 'figures/final/')
        print("📦 移动压缩包到figures/final/")
    
    # 整理其他图表相关文件
    chart_files = [
        'graph1.drawio.png',
        'graph2.drawio.png', 
        'graph3.drawio.png',
        'show.png',
        'ai.png',
        'background.webp',
        'background2.png'
    ]
    
    for file_name in chart_files:
        if os.path.exists(file_name):
            dest_path = os.path.join('figures', file_name)
            shutil.move(file_name, dest_path)
            print(f"🖼️  移动图片: {file_name}")

def create_summary():
    """创建整理后的项目结构说明"""
    
    summary_content = """# 项目文件夹整理说明

## 📁 新的目录结构

### 📚 docs/ - 核心文档
包含学术诚信报告、架构报告、可重现性指南等核心文档

### 📄 papers/ - 论文相关
包含CCF A类论文的各个版本、使用指南、数据更新文档等

### 📖 guides/ - 指南和说明
包含演示指南、部署指南、图表使用指南等

### 🔧 reports/fixes/ - 修复报告
包含各种修复报告和更新记录

### 📤 submission/ - 提交相关
包含提交清单和提交包说明

### 🛠️ scripts/ - 脚本文件
- `figure_generation/` - 图表生成脚本
- `analysis/` - 分析脚本
- `testing/` - 测试脚本  
- `startup/` - 启动脚本

### 📊 figures/ - 图表文件
- `final/` - 最终论文图表（专业配色，无标题）
- 其他图表和图片文件

### 📈 data/ - 数据文件
包含统计结果、事件数据、测试数据等

### ⚙️ config/ - 配置文件
包含Docker、Nginx、环境变量等配置文件

### 🎯 misc/ - 其他文件
包含CLI工具、演示文件、许可证等

## 🎨 图表特色
- 使用科学期刊顶级配色方案
- 去除标题避免顺序冲突
- 300 DPI高分辨率
- PNG + PDF双重格式

## 📦 使用说明
1. 所有文件已按功能分类整理
2. 图表文件集中在figures/目录
3. 脚本文件按用途分类到scripts/子目录
4. 文档文件按类型分类到不同目录

整理时间: 2024年9月16日
"""
    
    with open('FOLDER_ORGANIZATION_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print("📝 创建整理说明文档: FOLDER_ORGANIZATION_GUIDE.md")

def main():
    """主函数"""
    print("🚀 开始整理multi-agent-dsl-final项目文件夹")
    print("=" * 60)
    
    try:
        organize_files()
        create_summary()
        
        print("\n🎉 项目文件夹整理完成！")
        print("📁 新的目录结构更加清晰有序")
        print("📊 图表文件已集中管理")
        print("📝 详细说明请查看 FOLDER_ORGANIZATION_GUIDE.md")
        
    except Exception as e:
        print(f"❌ 整理过程中出错: {e}")

if __name__ == "__main__":
    main()
