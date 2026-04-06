---
name: "agent-video-validation"
description: "记录项目运行与验证流程。每次代码变更后调用，在 agent-video conda 环境中进入对应期数目录执行 python agent.py 验证。"
---

# Agent-Video 验证流程

## 适用范围
- 项目类型：Python 自媒体视频代码项目
- 每一期代码目录：以“数字th-”开头
- 入口文件：每一期目录下的 agent.py
- 运行环境：conda 虚拟环境 agent-video
- 技术栈：langchain 1.2.0、langgraph 1.0.5
- Python 版本：3.12

## 触发时机
- 每次修改或新增代码后
- 需要验证运行是否正常时

## 执行步骤
1. 进入对应的“数字th-”目录
2. 在 conda 环境 agent-video 中运行入口文件

```bash
conda run -n agent-video python agent.py
```

## 输出要求
- 汇报命令执行结果与关键输出
- 如果失败，定位错误信息并给出修复建议后再次验证
