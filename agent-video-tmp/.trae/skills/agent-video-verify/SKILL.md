---
name: "agent-video-verify"
description: "验证 Python 自媒体视频项目代码。每次改完代码后触发，进入对应“数字th-”目录并在 agent-video 环境执行 python agent.py。"
---

# Agent Video Verify

## 作用

在该项目中完成任何代码修改后，自动执行统一验证流程，确保改动可运行。

## 触发时机

- 只要本次任务包含代码改动，就在完成实现后、回复用户前执行验证
- 当用户提到“验证”“运行”“检查改动是否可用”时优先触发

## 项目约定

- 技术栈：langchain 1.2.0 + langgraph 1.05
- Python 版本：3.12
- 每一期代码目录命名：以“数字th-”开头（如 `10th-stream`、`11th-weather-mcp`）
- 每一期入口文件：`agent.py`
- Conda 环境：`agent-video`

## 验证流程

1. 先识别本次改动涉及的期数目录（目录名以 `th-` 规则匹配）。
2. 对每个涉及目录执行：
   - 切换到该目录
   - 在 `agent-video` 环境运行：`python agent.py`
3. 若无法直接激活 conda，则优先使用：
   - `conda run -n agent-video python agent.py`
4. 记录并汇总每个目录的运行结果（成功/失败与关键报错）。

## 执行标准

- 未执行验证不得宣告任务完成
- 若验证失败，优先修复后重新验证
- 最终反馈需明确：验证目录、执行命令、结果状态
