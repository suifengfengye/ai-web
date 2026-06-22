# Travel Agent 8 周工作与学习打卡计划

> 目标：围绕 `Travel Agent` 项目，用每天 `2 小时` 的投入，完成从前端工程师向 AI Agent 初级架构师的进阶。
>
> 这份计划不是“泛泛学习清单”，而是一个真正的架构师入门训练营：
>
> - 每天有明确的 `20 分钟阅读材料`
> - 每天有明确的 `项目开发任务`
> - 每天有明确的 `自媒体输出动作`
> - 每周有复盘与架构判断任务
>
> 使用方式：
>
> - 每天按当天任务推进。
> - 完成后直接告诉我“今天完成了第 X 周 Day X 的哪些事项”。
> - 我会继续在这份文档对应的事项后面帮你打 `✅`。

---

## 1. 总体规则

### 每天时间分配

- `20 分钟`：阅读指定文档，只看当天列出的官方资料
- `80 分钟`：直接做项目开发
- `20 分钟`：做复盘 + 自媒体记录

### 每周节奏

- `周一 ~ 周四`：开发 + 新知识学习
- `周五`：收尾本周功能 + 补文档
- `周六`：复盘 + 画图 + 内容整理
- `周日`：休息或轻复盘

### 自媒体创作规则

你有记录开发过程的习惯，这其实非常好，因为优秀架构师往往也有“表达能力”和“抽象能力”。

建议你把自媒体内容分成 3 类：

- `开发日志型`：今天做了什么、踩了什么坑
- `知识总结型`：比如“为什么这个项目先选 SQLite”
- `架构判断型`：比如“为什么我现在不引入 Redis”

每日只做轻量记录，不追求长文。原则是：

- 当天记录，不拖到以后
- 以项目为主，不写空洞鸡汤
- 输出你真实的判断过程

### 每日汇报模板

你每天完成后，可以直接用下面格式告诉我：

```text
今天完成：
1. 第 1 周 Day 1：初始化 monorepo
2. 第 1 周 Day 1：apps/web 跑起来了
3. 第 1 周 Day 1：完成了今日自媒体草稿

遇到的问题：
1. ...
2. ...

明天计划：
1. ...
2. ...
```

---

## 2. 阶段目标

### 第 1 阶段：搭出前后端和页面骨架

- 第 1 周：monorepo + 项目结构
- 第 2 周：用户端页面
- 第 3 周：管理后台页面

### 第 2 阶段：跑通 API 与数据层

- 第 4 周：FastAPI
- 第 5 周：SQLite

### 第 3 阶段：跑通 Agent 与 RAG

- 第 6 周：LangChain + SSE
- 第 7 周：Chroma + RAG

### 第 4 阶段：上线与架构复盘

- 第 8 周：部署、观测、系统复盘

---

## 3. 谷歌式架构训练原则

如果我是一个带你的 Google 高级架构师，我会要求你始终围绕下面 5 个问题学习和实现：

1. 这个需求真正要解决的问题是什么？
2. 当前最轻的可行方案是什么？
3. 这个方案的风险是什么？
4. 在什么信号出现后需要升级架构？
5. 现在的设计是否能留出升级路径？

你每天开发和写自媒体时，都尽量围绕这 5 个问题组织表达。

---

## 4. 8 周打卡清单

## 第 1 周：搭项目骨架

### 本周目标

- 建立 `pnpm + workspace` monorepo
- 建立 `apps/web`、`apps/admin`
- 建立 `packages/ui`、`packages/shared`
- 两个前端应用都能启动

### 本周重点

- `pnpm workspace`
- `Next.js App Router`
- monorepo 目录设计

### Day 1

阅读材料：

- pnpm Workspace: [https://pnpm.io/workspaces](https://pnpm.io/workspaces)
- Next.js App Router Getting Started: [https://nextjs.org/docs/app/getting-started/project-structure](https://nextjs.org/docs/app/getting-started/project-structure)

打卡清单：

- [ ] 阅读 20 分钟：pnpm workspace 和 Next.js 项目结构
- [ ] 初始化 `travel-agent` 前端 monorepo 目录结构
- [ ] 创建 `apps/web`
- [ ] 创建 `apps/admin`
- [ ] 写一页笔记：为什么拆 `web + admin`
- [ ] 自媒体记录：发布/整理一条“我为什么开始用项目驱动学习架构”的开发日志

### Day 2

阅读材料：

- pnpm Workspace Package.json: [https://pnpm.io/package_json#workspaces](https://pnpm.io/package_json#workspaces)
- TypeScript Project References: [https://www.typescriptlang.org/docs/handbook/project-references.html](https://www.typescriptlang.org/docs/handbook/project-references.html)

打卡清单：

- [ ] 阅读 20 分钟：workspace 配置和 TypeScript 共享工程
- [ ] 创建 `packages/ui`
- [ ] 创建 `packages/shared`
- [ ] 梳理共享内容：组件 / 类型 / API client / utils
- [ ] 写一页笔记：为什么要抽共享包
- [ ] 自媒体记录：输出一条“monorepo 到底解决了什么问题”

### Day 3

阅读材料：

- Next.js Installation: [https://nextjs.org/docs/app/getting-started/installation](https://nextjs.org/docs/app/getting-started/installation)
- Next.js Routing Fundamentals: [https://nextjs.org/docs/app/building-your-application/routing](https://nextjs.org/docs/app/building-your-application/routing)

打卡清单：

- [ ] 阅读 20 分钟：Next.js 安装与路由基础
- [ ] 跑通 `apps/web`
- [ ] 跑通 `apps/admin`
- [ ] 配好基础 `tsconfig` / `eslint` / `package.json`
- [ ] 记录遇到的初始化问题
- [ ] 自媒体记录：写一条“第一个 monorepo 初始化坑点总结”

### Day 4

阅读材料：

- Next.js Layouts and Pages: [https://nextjs.org/docs/app/building-your-application/routing/pages-and-layouts](https://nextjs.org/docs/app/building-your-application/routing/pages-and-layouts)
- Next.js Loading UI: [https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming)

打卡清单：

- [ ] 阅读 20 分钟：layout / page / loading 的基本概念
- [ ] 为 `web` 建立首页
- [ ] 为 `admin` 建立首页
- [ ] 写出两个应用的路由草图
- [ ] 写 5 句自己的理解：什么是 App Router
- [ ] 自媒体记录：录一条短内容“我怎么理解 Next.js 的 App Router”

### Day 5

阅读材料：

- Next.js Project Organization: [https://nextjs.org/docs/app/building-your-application/configuring/src-directory](https://nextjs.org/docs/app/building-your-application/configuring/src-directory)
- ESLint Getting Started: [https://eslint.org/docs/latest/use/getting-started](https://eslint.org/docs/latest/use/getting-started)

打卡清单：

- [ ] 阅读 20 分钟：项目组织和基础 lint 思路
- [ ] 整理 monorepo 目录说明
- [ ] 更新项目 README 或内部说明
- [ ] 回顾本周目录是否足够轻量
- [ ] 写一页本周总结
- [ ] 自媒体记录：输出“第 1 周阶段总结”

### Day 6

阅读材料：

- Turborepo Monorepo Handbook（选读）: [https://turbo.build/repo/docs](https://turbo.build/repo/docs)

打卡清单：

- [ ] 阅读 20 分钟：了解业界 monorepo 工程化思路
- [ ] 画出前端 monorepo 结构图
- [ ] 复盘：哪些地方先不抽象
- [ ] 列出下周用户端页面任务
- [ ] 自媒体记录：发一张架构草图并解释你的目录分层

### Day 7

阅读材料：

- Next.js Learn: [https://nextjs.org/learn](https://nextjs.org/learn)

打卡清单：

- [ ] 阅读 20 分钟：浏览 Next.js Learn 首页与目录
- [ ] 休息 / 轻复盘
- [ ] 补充本周未完成事项
- [ ] 自媒体记录：轻量复盘“我这周对前端架构最大的一个认识”

---

## 第 2 周：做用户端页面

### 本周目标

- 完成用户端对话页静态版
- 建立统一 UI 风格
- 熟悉 `Tailwind` 与 `shadcn/ui`

### 本周重点

- `Tailwind CSS`
- `shadcn/ui`
- 页面拆分与组件复用

### Day 1

阅读材料：

- Tailwind Installation: [https://tailwindcss.com/docs/installation](https://tailwindcss.com/docs/installation)
- Tailwind Utility-First Fundamentals: [https://tailwindcss.com/docs/utility-first](https://tailwindcss.com/docs/utility-first)

打卡清单：

- [ ] 阅读 20 分钟：Tailwind 安装和 utility-first 思想
- [ ] 在 `apps/web` 搭对话页基础布局
- [ ] 放置左侧聊天区 / 右侧结果区
- [ ] 写笔记：页面信息层级怎么拆
- [ ] 自媒体记录：发一条“为什么 AI 产品前端很适合用 Tailwind”

### Day 2

阅读材料：

- Tailwind Responsive Design: [https://tailwindcss.com/docs/responsive-design](https://tailwindcss.com/docs/responsive-design)
- Tailwind Hover, Focus, and Other States: [https://tailwindcss.com/docs/hover-focus-and-other-states](https://tailwindcss.com/docs/hover-focus-and-other-states)

打卡清单：

- [ ] 阅读 20 分钟：响应式和交互状态
- [ ] 实现聊天消息气泡
- [ ] 实现输入区
- [ ] 实现快捷操作按钮
- [ ] 记录 3 个想复用的组件
- [ ] 自媒体记录：输出一条“聊天页 UI 拆解过程”

### Day 3

阅读材料：

- shadcn/ui Introduction: [https://ui.shadcn.com/docs](https://ui.shadcn.com/docs)
- shadcn/ui Theming: [https://ui.shadcn.com/docs/theming](https://ui.shadcn.com/docs/theming)

打卡清单：

- [ ] 阅读 20 分钟：shadcn/ui 的设计哲学和主题方式
- [ ] 实现右侧行程摘要卡片
- [ ] 实现预算卡片
- [ ] 实现天气卡片
- [ ] 写笔记：结构化渲染比纯文本好在哪里
- [ ] 自媒体记录：输出“从文字到结构化卡片，我的设计思路”

### Day 4

阅读材料：

- shadcn/ui Button: [https://ui.shadcn.com/docs/components/button](https://ui.shadcn.com/docs/components/button)
- shadcn/ui Card: [https://ui.shadcn.com/docs/components/card](https://ui.shadcn.com/docs/components/card)
- shadcn/ui Input: [https://ui.shadcn.com/docs/components/input](https://ui.shadcn.com/docs/components/input)

打卡清单：

- [ ] 阅读 20 分钟：Button / Card / Input 组件
- [ ] 引入 `shadcn/ui` 常用组件
- [ ] 把按钮 / 卡片 / 输入框沉淀到 `packages/ui`
- [ ] 统一页面的颜色 / 圆角 / 间距
- [ ] 自媒体记录：写一条“为什么我不想自己从 0 造组件”

### Day 5

阅读材料：

- Tailwind Breakpoints: [https://tailwindcss.com/docs/breakpoints](https://tailwindcss.com/docs/breakpoints)
- Web.dev Responsive Design Basics: [https://web.dev/learn/design/](https://web.dev/learn/design/)

打卡清单：

- [ ] 阅读 20 分钟：响应式布局与断点
- [ ] 调整页面响应式
- [ ] 检查手机宽度下布局
- [ ] 补充空状态 / 加载状态草图
- [ ] 写一页本周总结
- [ ] 自媒体记录：发布“用户端页面第一版完成”

### Day 6

阅读材料：

- Framer Motion Docs（选读）: [https://motion.dev/docs](https://motion.dev/docs)

打卡清单：

- [ ] 阅读 20 分钟：了解动画库的边界，不急着深入
- [ ] 录一段自己对页面的讲解
- [ ] 复盘：哪些组件以后可以复用给管理后台
- [ ] 列出后台页面需求
- [ ] 自媒体记录：发一段页面讲解视频或图文

### Day 7

阅读材料：

- shadcn/ui Best Practices（主页目录继续浏览）: [https://ui.shadcn.com/docs/components](https://ui.shadcn.com/docs/components)

打卡清单：

- [ ] 阅读 20 分钟：浏览更多组件目录
- [ ] 休息 / 轻复盘
- [ ] 补本周未完成事项
- [ ] 自媒体记录：轻复盘“这一周我的前端工程感增强了什么”

---

## 第 3 周：做管理后台页面

### 本周目标

- 完成管理后台静态版
- 明确知识库管理的信息架构
- 建立“产品功能 -> 页面结构”的能力

### 本周重点

- 表格页
- 列表页
- 上传页
- 后台导航

### Day 1

阅读材料：

- shadcn/ui Table: [https://ui.shadcn.com/docs/components/table](https://ui.shadcn.com/docs/components/table)
- shadcn/ui Sidebar（若无官方可浏览 Blocks/布局思路）: [https://ui.shadcn.com/blocks](https://ui.shadcn.com/blocks)

打卡清单：

- [ ] 阅读 20 分钟：后台表格与布局参考
- [ ] 搭建后台整体布局
- [ ] 做左侧导航
- [ ] 做后台首页或知识库入口页
- [ ] 自媒体记录：输出“后台系统和用户端为什么是两种设计逻辑”

### Day 2

阅读材料：

- TanStack Table Docs（只看概念）: [https://tanstack.com/table/latest/docs/guide/introduction](https://tanstack.com/table/latest/docs/guide/introduction)

打卡清单：

- [ ] 阅读 20 分钟：理解后台表格的核心概念
- [ ] 做知识库文档列表页
- [ ] 展示文件名 / 状态 / 更新时间 / chunk 数
- [ ] 记录后台字段设计思路
- [ ] 自媒体记录：发一条“知识库后台字段怎么想出来的”

### Day 3

阅读材料：

- HTML File Input Basics（MDN）: [https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file)
- shadcn/ui Form: [https://ui.shadcn.com/docs/components/form](https://ui.shadcn.com/docs/components/form)

打卡清单：

- [ ] 阅读 20 分钟：文件上传表单的基本方式
- [ ] 做上传资料区域
- [ ] 做文档状态筛选
- [ ] 做搜索框
- [ ] 写笔记：后台和用户端的设计差异
- [ ] 自媒体记录：输出“后台上传区的交互设计”

### Day 4

阅读材料：

- shadcn/ui Dialog: [https://ui.shadcn.com/docs/components/dialog](https://ui.shadcn.com/docs/components/dialog)
- shadcn/ui Sheet: [https://ui.shadcn.com/docs/components/sheet](https://ui.shadcn.com/docs/components/sheet)

打卡清单：

- [ ] 阅读 20 分钟：弹窗和抽屉的使用场景
- [ ] 做知识库统计卡片
- [ ] 做文档详情页草图或弹窗
- [ ] 整理后台最小功能集
- [ ] 自媒体记录：发一条“什么时候用弹窗，什么时候用独立详情页”

### Day 5

阅读材料：

- Nielsen Norman Group 后台/数据表可用性相关文章（选读）: [https://www.nngroup.com/topic/data-tables/](https://www.nngroup.com/topic/data-tables/)

打卡清单：

- [ ] 阅读 20 分钟：理解数据表和后台可用性原则
- [ ] 检查后台页面的一致性
- [ ] 组件复用回收到 `packages/ui`
- [ ] 写一页本周总结
- [ ] 自媒体记录：输出“管理后台第一版完成”

### Day 6

阅读材料：

- Information Architecture Basics（选读）: [https://www.nngroup.com/articles/information-architecture-ia-basics/](https://www.nngroup.com/articles/information-architecture-ia-basics/)

打卡清单：

- [ ] 阅读 20 分钟：信息架构基础
- [ ] 画后台信息架构图
- [ ] 复盘：为什么后台要独立成一个应用
- [ ] 列出下周 API 需求
- [ ] 自媒体记录：发一张后台信息架构图并解释

### Day 7

阅读材料：

- Backstage / Admin 系统案例任选一篇阅读并做摘录

打卡清单：

- [ ] 阅读 20 分钟：吸收一个后台系统案例
- [ ] 休息 / 轻复盘
- [ ] 补本周未完成事项
- [ ] 自媒体记录：轻复盘“我开始理解后台系统的本质了什么”

---

## 第 4 周：搭 FastAPI 后端

### 本周目标

- 跑通真实 API
- 建立后端目录结构
- 从 demo 迈向产品化接口

### 本周重点

- `FastAPI`
- `Pydantic`
- 路由组织
- 错误处理

### Day 1

阅读材料：

- FastAPI First Steps: [https://fastapi.tiangolo.com/tutorial/first-steps/](https://fastapi.tiangolo.com/tutorial/first-steps/)
- Bigger Applications: [https://fastapi.tiangolo.com/tutorial/bigger-applications/](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

打卡清单：

- [ ] 阅读 20 分钟：FastAPI 基础与大项目结构
- [ ] 初始化 FastAPI 项目结构
- [ ] 拆出 `routers` / `schemas` / `services`
- [ ] 写笔记：后端目录为什么这样分
- [ ] 自媒体记录：输出“我如何把 FastAPI demo 升级成真实项目结构”

### Day 2

阅读材料：

- Request Body: [https://fastapi.tiangolo.com/tutorial/body/](https://fastapi.tiangolo.com/tutorial/body/)
- Response Model: [https://fastapi.tiangolo.com/tutorial/response-model/](https://fastapi.tiangolo.com/tutorial/response-model/)

打卡清单：

- [ ] 阅读 20 分钟：输入校验与响应模型
- [ ] 实现 `POST /plans`
- [ ] 实现 `GET /plans/{id}`
- [ ] 定义输入输出 schema
- [ ] 自媒体记录：发一条“为什么 schema 是 API 的边界”

### Day 3

阅读材料：

- File Uploads: [https://fastapi.tiangolo.com/tutorial/request-files/](https://fastapi.tiangolo.com/tutorial/request-files/)

打卡清单：

- [ ] 阅读 20 分钟：文件上传
- [ ] 实现 `GET /knowledge/list`
- [ ] 实现 `POST /knowledge/upload`
- [ ] 先用 mock 数据跑通
- [ ] 自媒体记录：输出“知识库上传接口设计草稿”

### Day 4

阅读材料：

- Handling Errors: [https://fastapi.tiangolo.com/tutorial/handling-errors/](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- Dependencies: [https://fastapi.tiangolo.com/tutorial/dependencies/](https://fastapi.tiangolo.com/tutorial/dependencies/)

打卡清单：

- [ ] 阅读 20 分钟：错误处理和依赖注入
- [ ] 加统一错误处理
- [ ] 加基础日志
- [ ] 理清 API 返回结构
- [ ] 自媒体记录：发一条“接口不是能返回数据就够了”

### Day 5

阅读材料：

- OpenAPI Docs（FastAPI 自动文档）: [https://fastapi.tiangolo.com/features/#automatic-docs](https://fastapi.tiangolo.com/features/#automatic-docs)

打卡清单：

- [ ] 阅读 20 分钟：自动 API 文档
- [ ] 前端联调至少 1 个接口
- [ ] 记录接口对前端的影响
- [ ] 写一页本周总结
- [ ] 自媒体记录：输出“第一条前后端联调成功记录”

### Day 6

阅读材料：

- Pydantic 文档首页（选读）: [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)

打卡清单：

- [ ] 阅读 20 分钟：理解 Pydantic 在后端中的位置
- [ ] 画 API 模块图
- [ ] 复盘：哪些逻辑该放 API 层，哪些不该放
- [ ] 列出 SQLite 表设计草案
- [ ] 自媒体记录：发一张 API 分层图并解释

### Day 7

阅读材料：

- FastAPI 官方 Tutorial 目录快速浏览: [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/)

打卡清单：

- [ ] 阅读 20 分钟：浏览官方教程目录，建立全局感
- [ ] 休息 / 轻复盘
- [ ] 补本周未完成事项
- [ ] 自媒体记录：轻复盘“我对服务端架构的理解开始变化了什么”

---

## 第 5 周：接 SQLite

### 本周目标

- 把业务数据真正存起来
- 建立基础数据建模能力
- 形成“轻量数据库也能支持 MVP”的判断

### 本周重点

- SQLite
- SQLAlchemy / SQLModel
- Alembic
- 数据表设计

### Day 1

阅读材料：

- SQLAlchemy 2.0 ORM Quick Start: [https://docs.sqlalchemy.org/en/20/orm/quickstart.html](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- Alembic Tutorial: [https://alembic.sqlalchemy.org/en/latest/tutorial.html](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

打卡清单：

- [ ] 阅读 20 分钟：ORM 和迁移工具基础
- [ ] 选定 ORM 方案
- [ ] 接入 SQLite
- [ ] 跑通第一版迁移
- [ ] 自媒体记录：输出“为什么这个项目先选 SQLite”

### Day 2

阅读材料：

- SQLite Overview: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
- SQLAlchemy Relationships（选读）: [https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)

打卡清单：

- [ ] 阅读 20 分钟：SQLite 特性与关系设计基础
- [ ] 建 `users`
- [ ] 建 `sessions`
- [ ] 建 `messages`
- [ ] 写笔记：会话和消息为什么分表
- [ ] 自媒体记录：发一条“从产品对象到数据表，我是怎么拆的”

### Day 3

阅读材料：

- SQLAlchemy Metadata / Mapped Classes（选读）
- SQLite CREATE INDEX: [https://www.sqlite.org/lang_createindex.html](https://www.sqlite.org/lang_createindex.html)

打卡清单：

- [ ] 阅读 20 分钟：模型定义与索引意识
- [ ] 建 `plans`
- [ ] 建 `knowledge_documents`
- [ ] 建 `tool_call_logs`
- [ ] 补必要索引
- [ ] 自媒体记录：输出“为什么索引不是越多越好”

### Day 4

阅读材料：

- SQLAlchemy Session Basics: [https://docs.sqlalchemy.org/en/20/orm/session_basics.html](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)

打卡清单：

- [ ] 阅读 20 分钟：数据库会话和 CRUD 基础
- [ ] 把 `plans` 接口接到真实数据库
- [ ] 把 `knowledge/list` 接到真实数据库
- [ ] 验证新增与查询流程
- [ ] 自媒体记录：发一条“接口真正连上数据库以后，我遇到的问题”

### Day 5

阅读材料：

- SQLite Appropriate Uses: [https://www.sqlite.org/whentouse.html](https://www.sqlite.org/whentouse.html)

打卡清单：

- [ ] 阅读 20 分钟：什么时候该用 SQLite
- [ ] 检查表设计是否过重或过度抽象
- [ ] 整理实体关系图草稿
- [ ] 写一页本周总结
- [ ] 自媒体记录：输出“为什么现在还不需要 PostgreSQL”

### Day 6

阅读材料：

- PostgreSQL 文档首页（只做全局认识）: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

打卡清单：

- [ ] 阅读 20 分钟：了解 PostgreSQL 作为未来升级路径
- [ ] 画 ER 图
- [ ] 复盘：为什么现在用 SQLite 足够
- [ ] 写出未来升级 PostgreSQL 的触发条件
- [ ] 自媒体记录：发一张 ER 图并解释你的建模逻辑

### Day 7

阅读材料：

- SQLModel 文档（若你选 SQLModel，可替换阅读）: [https://sqlmodel.tiangolo.com/](https://sqlmodel.tiangolo.com/)

打卡清单：

- [ ] 阅读 20 分钟：了解替代 ORM 思路
- [ ] 休息 / 轻复盘
- [ ] 补本周未完成事项
- [ ] 自媒体记录：轻复盘“数据库建模让我理解系统边界的地方”

---

## 第 6 周：接 LangChain + SSE

### 本周目标

- 跑通对话接口
- 实现流式输出
- 返回结构化 Agent 结果

### 本周重点

- `LangChain`
- SSE
- 结构化响应
- Agent 分层

### Day 1

阅读材料：

- FastAPI StreamingResponse: [https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
- MDN SSE: [https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

打卡清单：

- [ ] 阅读 20 分钟：SSE 与 StreamingResponse
- [ ] 设计 `/chat/stream` 的事件结构
- [ ] 定义 `status` / `partial_answer` / `final_result`
- [ ] 写笔记：为什么先用 SSE
- [ ] 自媒体记录：输出“为什么 AI 对话先用 SSE，而不是 WebSocket”

### Day 2

阅读材料：

- LangChain Overview: [https://python.langchain.com/docs/introduction/](https://python.langchain.com/docs/introduction/)
- FastAPI Streaming 相关资料继续补充

打卡清单：

- [ ] 阅读 20 分钟：复习 LangChain 整体结构
- [ ] 在 FastAPI 中实现 SSE 输出
- [ ] 前端接收并渲染流式内容
- [ ] 验证首 token 到达
- [ ] 自媒体记录：发一条“第一次看到自己的流式输出跑起来”

### Day 3

阅读材料：

- LangChain Structured Output: [https://python.langchain.com/docs/how_to/structured_output/](https://python.langchain.com/docs/how_to/structured_output/)

打卡清单：

- [ ] 阅读 20 分钟：结构化输出
- [ ] 接入 LangChain 基本链路
- [ ] 接入一个简单工具或 mock 工具
- [ ] 输出结构化结果对象
- [ ] 自媒体记录：输出“为什么 Agent 不应该只返回大段文本”

### Day 4

阅读材料：

- LangChain Tools: [https://python.langchain.com/docs/concepts/tools/](https://python.langchain.com/docs/concepts/tools/)

打卡清单：

- [ ] 阅读 20 分钟：工具在 Agent 中的位置
- [ ] 把结构化结果渲染到右侧卡片
- [ ] 存储会话消息
- [ ] 记录 Agent 输出格式设计思路
- [ ] 自媒体记录：发一条“Agent 层和 API 层到底怎么分工”

### Day 5

阅读材料：

- LangChain Streaming（按官网当前目录选择）: [https://python.langchain.com/docs/](https://python.langchain.com/docs/)

打卡清单：

- [ ] 阅读 20 分钟：补 streaming 相关概念
- [ ] 测一次从输入到流式完成的完整链路
- [ ] 补错误处理
- [ ] 写一页本周总结
- [ ] 自媒体记录：输出“第一个能流式响应的 Agent 接口”

### Day 6

阅读材料：

- LangGraph Overview（只建立认知）: [https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)

打卡清单：

- [ ] 阅读 20 分钟：了解未来的状态编排方向
- [ ] 画 Agent 调用链路图
- [ ] 复盘：哪些职责属于 Agent，哪些属于 API
- [ ] 列出下周 RAG 接入任务
- [ ] 自媒体记录：发一张 Agent 调用图并解释

### Day 7

阅读材料：

- SSE / LangChain 任选一篇官方文档回顾

打卡清单：

- [ ] 阅读 20 分钟：复盘本周核心知识点
- [ ] 休息 / 轻复盘
- [ ] 补本周未完成事项
- [ ] 自媒体记录：轻复盘“我第一次开始像架构师一样看 Agent 系统”

---

## 第 7 周：接 Chroma 与 RAG

### 本周目标

- 让后台上传的资料真正参与问答
- 掌握一条完整 RAG 闭环
- 能排查基础检索问题

### 本周重点

- 文档切分
- embedding
- Chroma
- 引用来源

### Day 1

阅读材料：

- Chroma Docs: [https://docs.trychroma.com/](https://docs.trychroma.com/)
- LangChain RAG Overview: [https://python.langchain.com/docs/concepts/rag/](https://python.langchain.com/docs/concepts/rag/)

打卡清单：

- [ ] 阅读 20 分钟：Chroma 和 RAG 基本概念
- [ ] 设计知识库入库流程
- [ ] 文档上传后完成切分
- [ ] 写笔记：chunk 大小如何权衡
- [ ] 自媒体记录：输出“为什么我在这个项目里先选 Chroma”

### Day 2

阅读材料：

- LangChain Text Splitters: [https://python.langchain.com/docs/concepts/text_splitters/](https://python.langchain.com/docs/concepts/text_splitters/)
- LangChain Embeddings: [https://python.langchain.com/docs/concepts/embedding_models/](https://python.langchain.com/docs/concepts/embedding_models/)

打卡清单：

- [ ] 阅读 20 分钟：文本切分和 embedding 模型
- [ ] 生成 embedding
- [ ] 写入 Chroma
- [ ] 验证向量入库成功
- [ ] 自媒体记录：发一条“我的第一批向量数据入库了”

### Day 3

阅读材料：

- LangChain Vector Stores: [https://python.langchain.com/docs/concepts/vectorstores/](https://python.langchain.com/docs/concepts/vectorstores/)
- Chroma Query Basics: [https://docs.trychroma.com/docs/querying-collections/query-and-get](https://docs.trychroma.com/docs/querying-collections/query-and-get)

打卡清单：

- [ ] 阅读 20 分钟：检索与查询基础
- [ ] 在聊天时接入检索
- [ ] 返回 top-k 内容
- [ ] 加 metadata 或来源信息
- [ ] 自媒体记录：输出“RAG 不只是检索，它是可解释性的一部分”

### Day 4

阅读材料：

- LangChain Retrieval 概念页: [https://python.langchain.com/docs/concepts/retrieval/](https://python.langchain.com/docs/concepts/retrieval/)

打卡清单：

- [ ] 阅读 20 分钟：retrieval 的核心概念
- [ ] 前端展示引用来源
- [ ] 测试 3 个真实问题
- [ ] 记录召回表现
- [ ] 自媒体记录：发一条“我怎么判断 RAG 有没有真正生效”

### Day 5

阅读材料：

- LangChain RAG How-to 目录浏览: [https://python.langchain.com/docs/how_to/#qa-with-rag](https://python.langchain.com/docs/how_to/#qa-with-rag)

打卡清单：

- [ ] 阅读 20 分钟：补 RAG 实战技巧
- [ ] 调整切分或检索参数
- [ ] 排查一次“为什么没召回到”
- [ ] 写一页本周总结
- [ ] 自媒体记录：输出“RAG 的第一次调优记录”

### Day 6

阅读材料：

- Qdrant Docs（只建立升级认知）: [https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)

打卡清单：

- [ ] 阅读 20 分钟：理解 Qdrant 作为未来升级路线
- [ ] 画 RAG 链路图
- [ ] 复盘：为什么现在 Chroma 最合适
- [ ] 写出未来升级 Qdrant 的触发条件
- [ ] 自媒体记录：发一张 RAG 链路图并解释

### Day 7

阅读材料：

- 任意一篇你觉得最有帮助的 RAG 官方文档回顾

打卡清单：

- [ ] 阅读 20 分钟：RAG 知识回顾
- [ ] 休息 / 轻复盘
- [ ] 补本周未完成事项
- [ ] 自媒体记录：轻复盘“RAG 让我开始真正理解 AI 应用工程”

---

## 第 8 周：部署、观测、架构复盘

### 本周目标

- 项目上线可访问
- 补基础观测
- 形成完整系统认知和架构表达能力

### 本周重点

- `Vercel`
- `Render / Railway / Fly.io`
- 持久化磁盘
- 架构复盘

### Day 1

阅读材料：

- Vercel Docs: [https://vercel.com/docs](https://vercel.com/docs)
- Render Docs: [https://render.com/docs](https://render.com/docs)

打卡清单：

- [ ] 阅读 20 分钟：前后端部署平台总览
- [ ] 确定部署方案
- [ ] 准备环境变量清单
- [ ] 写笔记：前后端为什么分开部署
- [ ] 自媒体记录：输出“为什么 Python Agent 不直接塞到前端部署平台”

### Day 2

阅读材料：

- Vercel Next.js Guide: [https://vercel.com/docs/frameworks/nextjs](https://vercel.com/docs/frameworks/nextjs)

打卡清单：

- [ ] 阅读 20 分钟：Next.js 在 Vercel 的部署方式
- [ ] 部署 `apps/web`
- [ ] 部署 `apps/admin`
- [ ] 验证页面可访问
- [ ] 自媒体记录：发一条“前端首次上线成功”

### Day 3

阅读材料：

- Render Web Services: [https://render.com/docs/web-services](https://render.com/docs/web-services)
- Render Disks: [https://render.com/docs/disks](https://render.com/docs/disks)

打卡清单：

- [ ] 阅读 20 分钟：后端服务和持久化磁盘
- [ ] 部署 FastAPI
- [ ] 配置持久化磁盘
- [ ] 验证 SQLite 与 Chroma 数据不会丢
- [ ] 自媒体记录：输出“本地能跑和线上能跑是两回事”

### Day 4

阅读材料：

- Sentry Docs（选读）: [https://docs.sentry.io/](https://docs.sentry.io/)
- OpenTelemetry Docs（选读）: [https://opentelemetry.io/docs/](https://opentelemetry.io/docs/)

打卡清单：

- [ ] 阅读 20 分钟：了解最小化监控与错误追踪
- [ ] 接基础日志
- [ ] 接错误监控或最小化异常记录
- [ ] 记录部署踩坑
- [ ] 自媒体记录：输出“为什么监控不是后期再说”

### Day 5

阅读材料：

- Twelve-Factor App（选读）: [https://12factor.net/](https://12factor.net/)

打卡清单：

- [ ] 阅读 20 分钟：建立服务部署与配置分离意识
- [ ] 做一次端到端完整测试
- [ ] 整理上线说明
- [ ] 写一页本周总结
- [ ] 自媒体记录：发一条“我的 Travel Agent MVP 上线了”

### Day 6

阅读材料：

- C4 Model（选读）: [https://c4model.com/](https://c4model.com/)

打卡清单：

- [ ] 阅读 20 分钟：理解系统图和架构表达方法
- [ ] 画系统设计图
- [ ] 画技术架构图
- [ ] 画数据流与调用链路图
- [ ] 做一次项目整体复盘
- [ ] 自媒体记录：输出“我如何向别人讲清楚这个系统”

### Day 7

阅读材料：

- 回顾 `03-tech-stack.md` 与 `04-architect-growth-roadmap.md`

打卡清单：

- [ ] 阅读 20 分钟：回顾自己的技术选型与成长目标
- [ ] 总结 8 周学习成果
- [ ] 写出“我已经掌握了什么、下一步学什么”
- [ ] 列出架构升级路线：`SQLite -> PostgreSQL`、`Chroma -> Qdrant`
- [ ] 自媒体记录：发布 8 周总结长文或长视频提纲

---

## 5. 每周复盘模板

每周建议你自己写一次复盘，可以按这个模板：

```text
本周完成：
1. ...
2. ...
3. ...

本周学会：
1. ...
2. ...

遇到问题：
1. ...
2. ...

本周的架构判断：
1. 这个需求真正要解决的问题是什么？
2. 当前最轻的可行方案是什么？
3. 为什么现在不做更重的方案？
4. 未来出现什么信号时需要升级？

自媒体输出：
1. 本周发布了什么？
2. 哪条内容最有价值？
3. 下周想重点记录什么？

下周计划：
1. ...
2. ...
3. ...
```

---

## 6. 自媒体内容模板

如果你每天不想花太多时间构思，可以直接套模板。

### 模板 1：开发日志

```text
今天我在做 Travel Agent 的第 X 周 Day X。
今天主要完成了：
1. ...
2. ...

我遇到的一个问题：
...

我最后怎么解决：
...

我今天最大的一个架构认识：
...
```

### 模板 2：技术判断

```text
为什么我在这个阶段选择了 XXX，而不是 YYY？

当前需求：
...

更轻的方案：
...

为什么当前足够：
...

什么时候会升级：
...
```

### 模板 3：每周总结

```text
这是我做 Travel Agent 的第 X 周。

这周完成了：
1. ...
2. ...
3. ...

这周真正学会了：
1. ...
2. ...

这周我开始理解的架构问题：
...

下周继续：
...
```

---

## 7. 最终验收标准

8 周完成后，你至少应该达到这些标准：

- [ ] 能讲清楚 `Travel Agent` 的系统模块划分
- [ ] 能独立搭建 `web + admin + api` 的基本结构
- [ ] 能用 `SQLite` 建立业务数据模型
- [ ] 能用 `LangChain + Chroma` 跑通一条基础 RAG 闭环
- [ ] 能解释为什么当前技术选型是轻量且合理的
- [ ] 能说出未来的升级方向，而不是一开始就做重架构
- [ ] 能把开发过程转化为持续的高质量自媒体内容

如果这些都达成，你就已经不是“只会写页面的前端”，而是具备 AI Agent 初级架构师的雏形了。
