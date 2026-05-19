# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中操作代码时提供指导。

 ## 项目概述

一个用于测试和实验的极简 Python 项目。当前仅包含一个 hello-world 脚本。
Python 学习笔记项目。用于记录每日 Python 学习内容，包含学习笔记（笔记.txt）和 AI 自动生成的学习重点总结
（cc总结.txt）。

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `笔记.txt` | 每日学习记录，由用户手动填写 |
| `cc总结.txt` | AI 根据笔记.txt 自动生成的当日学习重点总结 |
| `程序` | 用于存放项目代码 |
| `CLAUDE.md` | 项目指导文件 |

## 工作流程

1. 用户在 `笔记.txt` 中记录当天学习内容
2. Claude Code 读取 `笔记.txt`，总结当日重点，写入 `cc总结.txt`

## 运行

```bash
python hello_world.py
```

## 代码风格

简单的 Python 脚本，无外部依赖
无构建系统、打包或虚拟环境
除非复杂度需要，否则优先使用单文件脚本
