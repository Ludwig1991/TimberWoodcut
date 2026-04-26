# Trellis AI 编程工作流框架办公整理文档
## 一、核心概述
Trellis 是一款面向 AI 编程场景的**开源工作流操作系统**，本质是为 AI 代码工具赋予“长期项目记忆”与“团队协作标准”的框架，支持 Claude Code、Cursor、Windsurf、Copilot 等 14 个主流 AI 编程平台，核心解决 AI 写代码时的上下文丢失、规范不统一、协作混乱等问题。

## 二、解决的核心痛点
| 痛点场景 | 具体表现 |
|----------|----------|
| 上下文丢失 | 每次开启新会话，AI 完全忘记之前的项目进度与工作内容 |
| 规范不落地 | AI 不会主动读取项目的 AGENTS.md、CLAUDE.md 等规范文档，代码风格/架构不符合要求 |
| 多人协作混乱 | 团队协作时，AI 无法理解统一的项目规范，不同开发者的代码风格/逻辑割裂 |
| 项目失控 | 代码越写越乱，AI 与开发者都不清楚当前核心任务与进度 |

## 三、核心目录结构
```
.trellis/
├── spec/           # 项目规范文档（AI 每次对话必须自动读取）
│   ├── spec.md      # 项目主规范
│   ├── backend/    # 后端开发专项规范
│   ├── frontend/    # 前端开发专项规范
│   └── guides/      # 开发思维指南与最佳实践
├── tasks/           # 任务管理目录（存储当前/历史任务）
│   └── 04-21-my-task/
│       └── task.json
├── workspace/       # 开发者独立工作区（每人独立日志，互不干扰）
│   └── 风中梧桐/
│       └── journal-1.md   # 单条会话记录
└── scripts/         # 自动化工具脚本
    ├── get_context.py    # 获取当前项目上下文
    ├── task.py           # 任务创建/启动/管理
    └── add_session.py    # 记录会话日志
```

## 四、当前安装与配置状态
| 配置项 | 状态 | 补充说明 |
|--------|------|----------|
| Trellis CLI | ✅ 已全局安装 | 可直接在终端调用 Trellis 命令 |
| .trellis/ 目录 | ✅ 已创建 | 核心工作流目录已生成 |
| AGENTS.md | ✅ 已注入 Trellis 指令块 | 新会话自动读取项目规范 |
| 开发者身份 | ✅ 已绑定“风中梧桐” | 独立 workspace 已创建 |
| Claude Code 配置 | ✅ 已完成 | 支持 Claude Code 平台调用 |
| Cursor 配置 | ✅ 已完成 | 支持 Cursor 平台调用 |

## 五、核心使用方法
### （一）新会话启动：自动加载项目上下文
```bash
# 1. 获取当前项目完整上下文
python3 ./.trellis/scripts/get_context.py

# 2. 手动确认项目主规范（可选，AI 已自动读取）
cat .trellis/spec/spec.md
```

### （二）任务管理：创建并启动当前任务
```bash
# 1. 创建新任务（自动生成任务目录与 task.json）
python3 ./.trellis/scripts/task.py create "测试Trellis功能" --slug test-trellis

# 2. 启动任务（设为当前核心任务，新会话自动识别）
python3 ./.trellis/scripts/task.py start test-trellis

# 3. 查看所有任务列表
python3 ./.trellis/scripts/task.py list
```

### （三）会话结束：记录工作进度
```bash
# 记录本次会话的标题、关联 commit 与核心总结
python3 ./.trellis/scripts/add_session.py \
  --title "完成Trellis初始化" \
  --commit "abc1234" \
  --summary "安装并配置了Trellis框架"
```

## 六、关键设计理念
| 设计点 | 核心作用 |
|--------|----------|
| Spec 自动注入 | AI 每次对话前自动读取 `.trellis/spec/` 下的所有规范，无需手动提醒“看规范” |
| 当前任务机制 | 通过 `task.py start` 绑定任务后，新会话自动识别当前核心工作，无需重复说明 |
| 日志自动分页 | 单条日志文件超过 2000 行时自动创建新文件，避免单文件过大 |
| 多开发者支持 | 每人独立 `workspace/` 目录，日志与进度互不干扰 |
| 跨平台兼容 | 同一套 `.trellis/` 结构支持 14 个主流 AI 编程工具，无需重复配置 |

## 七、核心工作规则
1.  **写代码前必须读 Spec**：AI 未读取 `.trellis/spec/` 规范前，不得开始代码编写；
2.  **Git Commit 由人类执行**：AI 不自动执行 git commit 操作，需开发者手动确认后提交；
3.  **单任务推进**：同一时间仅启动一个核心任务，避免同时推进多个无关任务导致混乱；
4.  **日志不超 2000 行**：单条会话日志自动分页，无需手动拆分。

## 八、一句话核心总结
Trellis 的核心是三件事：**让 AI 先读规范再动手（.trellis/spec/）、记住当前任务（.trellis/tasks/）、记录会话日志（.trellis/workspace/）**，本质是为 AI 编程赋予“项目长期记忆”的工作流操作系统。
