# Multi-Agent DSL Framework 图表集合

## 📊 性能分析图表 (Python生成)

### 1. 吞吐量对比图
- **文件**: `throughput_comparison.png/pdf`
- **标题**: Figure 1. Throughput Comparison Across Frameworks
- **描述**: 对比不同框架的吞吐量性能
- **数据**: LangChain, CrewAI, AutoGen, Our DSL
- **特点**: 简洁的性能提升标注

### 2. 可扩展性分析图
- **文件**: `scalability_analysis.png/pdf`
- **标题**: Figure 2. Scalability Analysis: Throughput vs Number of Agents
- **描述**: 展示系统在不同智能体数量下的可扩展性
- **数据**: 1-1000个智能体的吞吐量变化
- **特点**: 线性+对数双坐标显示

### 3. 缓存性能分析图
- **文件**: `cache_performance.png/pdf`
- **标题**: Figure 3a. Cache Hit Rate by Access Pattern / Figure 3b. Cache Latency by Access Pattern
- **描述**: PAAC算法在不同访问模式下的性能
- **数据**: 顺序、随机、重复访问的命中率和延迟
- **特点**: 双子图对比展示

### 4. 延迟分析图
- **文件**: `latency_analysis.png/pdf`
- **标题**: Figure 4. Latency Distribution by Task Complexity
- **描述**: 不同任务复杂度下的延迟分布
- **数据**: 简单、中等、复杂、非常复杂任务的延迟
- **特点**: 箱线图+平均值标注

### 5. 算法性能对比图
- **文件**: `algorithm_comparison.png/pdf`
- **标题**: Figure 5. Algorithm Performance Comparison
- **描述**: 各算法模块的性能对比
- **数据**: AW-RR, PAAC, CRL, 集成系统
- **特点**: 相对性能分数展示

### 6. 内存使用分析图
- **文件**: `memory_usage.png/pdf`
- **标题**: Figure 6. Memory Usage vs Number of Agents
- **描述**: 内存使用随智能体数量的变化
- **数据**: 1-100个智能体的内存消耗
- **特点**: 线性增长趋势

### 7. 性能总结雷达图
- **文件**: `performance_summary.png/pdf`
- **标题**: Figure 7. Performance Summary Comparison
- **描述**: 综合性能指标对比
- **数据**: 吞吐量、可扩展性、缓存命中率、延迟、内存效率
- **特点**: 雷达图展示多维度性能

## 🏗️ 系统架构图表 (Mermaid生成，已改好名字)

### 8. 系统架构图
- **文件**: `diagrams/mermaid_charts/Figure 8.png`
- **标题**: Figure 8. Multi-Agent DSL Framework Architecture
- **状态**: ✅ 已改好名字
- **描述**: Multi-Agent DSL Framework整体架构
- **内容**: DSL层、运行时层、算法层、执行层
- **特点**: 四层架构清晰展示

### 9. AW-RR算法流程图
- **文件**: `diagrams/mermaid_charts/Figure 9.png`
- **标题**: Figure 9. AW-RR Algorithm Flow
- **状态**: ✅ 已改好名字
- **描述**: 自适应加权轮询算法流程
- **内容**: 负载计算、权重更新、智能体选择
- **特点**: 循环反馈机制

### 10. PAAC缓存算法架构图
- **文件**: `diagrams/mermaid_charts/Figure 10.png`
- **标题**: Figure 10. PAAC Cache Algorithm Architecture
- **状态**: ✅ 已改好名字
- **描述**: 模式感知自适应缓存算法
- **内容**: 访问历史分析、相关性计算、淘汰决策
- **特点**: 多维度评分机制

### 11. CRL协作学习机制图
- **文件**: `diagrams/mermaid_charts/Figure 11.png`
- **标题**: Figure 11. CRL Collaborative Learning Mechanism
- **状态**: ✅ 已改好名字
- **描述**: 协作强化学习机制
- **内容**: 相似性计算、知识转移、Q表更新
- **特点**: 智能体间协作学习

### 12. 任务执行流程图
- **文件**: `diagrams/mermaid_charts/Figure 12.png`
- **标题**: Figure 12. Task Execution Flow
- **状态**: ✅ 已改好名字
- **描述**: 任务执行完整流程
- **内容**: DSL程序解析、缓存检查、任务执行、状态更新
- **特点**: 包含缓存命中和未命中两种路径

### 13. 性能优化策略图
- **文件**: `diagrams/mermaid_charts/Figure 13.png`
- **标题**: Figure 13. Performance Optimization Strategy
- **状态**: ✅ 已改好名字
- **描述**: 综合性能优化策略
- **内容**: 负载均衡、缓存优化、学习优化、系统优化
- **特点**: 四维度优化策略汇总

### 14. 实验评估框架图
- **文件**: `diagrams/mermaid_charts/Figure 14.png`
- **标题**: Figure 14. Experimental Evaluation Framework
- **状态**: ✅ 已改好名字
- **描述**: 实验评估框架设计
- **内容**: 可扩展性测试、基线对比、缓存性能、延迟分析
- **特点**: 多维度性能评估体系

### 15. 框架组件交互图
- **文件**: `diagrams/mermaid_charts/Figure 15.png`
- **标题**: Figure 15. Framework Component Interaction
- **状态**: ✅ 已改好名字
- **描述**: 框架组件交互关系
- **内容**: DSL API、TaskBuilder、Scheduler、算法模块、缓存管理
- **特点**: 组件间数据流和交互关系

## 🎨 其他资源图片

### 项目标识
- **文件**: `ai.png`
- **描述**: AI/智能体相关标识图片
- **用途**: 项目展示、文档配图

### 背景图片
- **文件**: `background2.png`
- **描述**: 项目背景图片
- **用途**: 演示文稿、网页背景

### 展示图片
- **文件**: `show.png`
- **描述**: 项目展示用图片
- **用途**: 演示、宣传材料

## 📁 文件组织结构

```
figures/
├── README.md                    # 本说明文档
├── ai.png                       # AI标识图片
├── background2.png             # 背景图片
├── show.png                     # 展示图片
├── throughput_comparison.png    # 吞吐量对比图
├── throughput_comparison.pdf    # 吞吐量对比图(PDF)
├── scalability_analysis.png     # 可扩展性分析图
├── scalability_analysis.pdf     # 可扩展性分析图(PDF)
├── cache_performance.png        # 缓存性能分析图
├── cache_performance.pdf        # 缓存性能分析图(PDF)
├── latency_analysis.png         # 延迟分析图
├── latency_analysis.pdf         # 延迟分析图(PDF)
├── algorithm_comparison.png     # 算法性能对比图
├── algorithm_comparison.pdf     # 算法性能对比图(PDF)
├── memory_usage.png             # 内存使用分析图
├── memory_usage.pdf             # 内存使用分析图(PDF)
├── performance_summary.png     # 性能总结雷达图
├── performance_summary.pdf      # 性能总结雷达图(PDF)
└── diagrams/                    # 架构图表目录
    ├── system_architecture.png  # 旧版系统架构图
    ├── awrr_algorithm_flow.png  # 旧版AW-RR算法流程图
    ├── paac_cache_algorithm.png # 旧版PAAC缓存算法架构图
    └── mermaid_charts/          # Mermaid图表目录
        ├── chart1_system_architecture.png              # 系统架构图
        ├── chart2_awrr_algorithm_flow.png             # AW-RR算法流程图
        ├── chart3_paac_cache_algorithm.png            # PAAC缓存算法架构图
        ├── chart4_crl_collaborative_learning.png      # CRL协作学习机制
        ├── chart5_task_execution_flow.png             # 任务执行流程图
        ├── chart6_performance_optimization_strategy.png # 性能优化策略图
        ├── chart7_experimental_evaluation_framework.png # 实验评估框架图
        └── chart8_framework_component_interaction.png   # 框架组件交互图
```

## 🎯 使用建议

### 论文插图
- **性能数据图表**: 直接使用PNG格式，300 DPI分辨率
- **架构流程图**: 使用diagrams目录中的图片
- **学术标准**: 所有图表都有清晰的标题、图例和标注

### 演示文稿
- **PNG格式**: 用于PPT、网页展示
- **PDF格式**: 用于高质量印刷、学术发表
- **背景图片**: 用于演示文稿背景

### 文档配图
- **README**: 使用ai.png作为项目标识
- **技术文档**: 使用diagrams目录中的架构图
- **性能报告**: 使用性能分析图表

## 🔧 图表生成

所有Python生成的图表都可以通过以下命令重新生成：

```bash
python3 generate_figures.py
```

Mermaid图表需要复制代码到在线编辑器生成，代码位于 `mermaid_diagrams.md` 文件中。

## 📊 图表质量

- **分辨率**: 300 DPI以上
- **格式**: PNG和PDF双格式
- **颜色**: 学术友好的配色方案
- **字体**: 清晰易读的字体
- **标注**: 重要数据点标注
- **一致性**: 保持图表风格一致

---

**最后更新**: 2024年9月12日  
**维护者**: Multi-Agent DSL Framework Team
