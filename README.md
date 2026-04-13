# deep-research-skill

面向 **OpenClaw / Codex 类 Agent** 的**决策导向深度研究技能仓库**。

它不是一个“搜一下然后总结”的提示词集合，而是一套把研究任务收紧为**可路由、可审计、可迭代、可交付**流程的方法系统：先识别任务类型，再绑定研究纪律、审计门槛、失败样例和交付管线，最后输出更像 **decision memo** 而不是“信息堆砌型综述”。

---

## 这个仓库在解决什么问题

很多“deep research”最后会滑向几个常见失败：

- 看起来很完整，其实没有回答真正的决策问题
- 该查“当前状态”的任务，混入了过时信息
- 引用很多，但 claim 和 source 之间并不真正可追溯
- 缺少反证、替代解释、unknown 约束
- 报告写得像行业综述，不像可执行的判断备忘录
- 最终 PDF / markdown 交付层仍然有脏痕迹、占位符、结构泄漏

这个 skill 的目标，就是把这些失败模式显式化，并沉淀成：

- **route（任务路由）**
- **discipline（研究纪律）**
- **checklist（交付审计）**
- **eval（真实坏例子回灌）**
- **script（交付渲染与验证）**

---

## 核心能力

### 1. 决策导向，而不是摘要导向
不是把信息搜齐就结束，而是把任务收紧成：

- 要判断什么
- 用什么比较单位判断
- 哪些事实必须 current-state verified
- 哪些结论只是 inferred / scenario assumption / illustrative calculation
- 什么反证会削弱当前结论
- 什么 unknown 会限制结论强度

### 2. 任务路由明确
仓库会把不同任务族分开处理，而不是套一个泛用模板。

典型覆盖包括：

- shortlist / option selection
- market entry / regional expansion
- market outlook / industry evolution
- listed-company / moat / monopoly-style judgment
- uncertainty-sensitive、forward-looking、comparative research

### 3. 研究纪律可复用
`references/` 中沉淀的是可反复调用的方法，而不是一次性提示词。

例如：

- source quality / source traceability
- current-state verification
- counter-evidence
- quantitative role labeling
- claim matrix
- route activation / preflight
- market sizing / market share discipline
- ranking and current-claims discipline

### 4. 最终交付有审计门槛
`checklists/` 不是装饰。它们的作用是防止“研究过程还行，但最后交付还是脏”。

会重点拦截：

- 强断言无足够 source support
- freshness / date discipline 不够
- claim 不可追溯
- 反证和不确定性没有进入最终判断
- placeholder residue / citation artifact / delivery cleanliness 问题

### 5. 用真实坏例子驱动迭代
`evals/` 不是演示材料，而是把真实失败案例转成规则、模板、检查项和回归资产。

这意味着这个仓库的演进逻辑不是“继续堆规则”，而是：

- 发现真实 bad case
- 先判断是 policy gap 还是 execution drift
- 再决定改 route、reference、checklist、eval 还是 script

---

## 仓库结构

```text
.
├── SKILL.md                # 主工作流脊柱：给 Agent 的入口说明
├── ROUTING-MATRIX.md       # 任务路由、附加 discipline、审计绑定
├── ARCHITECTURE.md         # 分层架构视图
├── SYSTEM-MAP.md           # 全仓库结构地图 / 问题域地图
├── references/             # 可复用研究方法、模板、纪律说明
├── checklists/             # 交付前审计门槛
├── evals/                  # 坏例子、回归资产、对比蒸馏沉淀
├── examples/               # 代表性任务形状示例
├── scripts/                # markdown / PDF 渲染与验证工具
├── CHANGELOG.md            # 重要行为变化记录
└── ROADMAP.md              # 后续改进方向
```

---

## 推荐阅读顺序

如果你是第一次看这个仓库，建议按这个顺序：

1. **`README.md`**：看清仓库目标与结构
2. **`SKILL.md`**：看 Agent 实际执行时的工作流脊柱
3. **`ROUTING-MATRIX.md`**：看任务如何分流，以及每类任务挂什么 discipline / audit
4. **`ARCHITECTURE.md`**：看仓库分层与职责边界
5. **`SYSTEM-MAP.md`**：看问题域、失败族和干预路径
6. 按任务需要再进入 `references/`、`checklists/`、`evals/`、`scripts/`

---

## 这个仓库怎么协同工作

它的大致执行顺序是：

1. **`SKILL.md`** 定义通用工作流脊柱
2. **`ROUTING-MATRIX.md`** 识别当前任务族，并挂上对应 discipline / audit
3. **`references/`** 提供方法、模板、claim discipline 与研究约束
4. **`checklists/`** 检查最终产物是否真的达到交付标准
5. **`evals/`** 把真实失败沉淀成可复盘、可回归的资产
6. **`scripts/`** 负责 markdown → PDF 等交付层问题

一句话概括：
**route 决定你该怎么研究，checklist 决定你能不能交付，eval 决定你会不会重复犯错。**

---

## 适合什么任务

这个 skill 更适合下面这类任务：

- 不是只要信息，而是要**判断 / 选择 / 优先级 / 建议**
- 问题对**当前状态**敏感，旧资料会误导结论
- 需要比较多个选项，而不是单点介绍
- 需要把**反证、未知项、证据强弱**放进最终结论
- 最终产物要像 **memo / recommendation / decision support**，而不是普通综述

例如：

- “哪个国家最适合先进入，为什么不是另外两个？”
- “未来 12 个月这个市场更可能怎么演化？关键变量是什么？”
- “这家公司是否真的具备稀缺 / 垄断 / 不可替代特征？”
- “几个候选方案里，默认首选是谁，什么变化会让排名翻转？”

---

## 不想把它做成什么

这个仓库**不追求**：

- 把所有研究问题都硬塞进同一个模板
- 用更多提示词长度代替方法清晰度
- 用“看起来像研究”的长文掩盖 decision drift
- 用 provider 切换代替 search objective / query shape 的思考
- 把 final-delivery cleanliness 当成小问题

---

## 如何演进这个仓库

推荐按“问题最靠近哪里，就改哪里”的方式迭代：

- **任务激活不准** → 改 `ROUTING-MATRIX.md`
- **方法不够强** → 改 `references/`
- **最后成稿仍然脏** → 改 `checklists/`
- **失败模式仍模糊** → 加 `evals/`
- **内容没问题但 PDF / HTML 渲染坏掉** → 改 `scripts/`

尽量避免“大杂烩式 PR”。

更稳的方式通常是：

- route / policy 一条 PR
- checklist / audit 一条 PR
- rendering / PDF pipeline 一条 PR

---

## 维护原则

- 重要行为变化写入 `CHANGELOG.md`
- 明确下一步改进放进 `ROADMAP.md`
- 真实坏例子尽量配套新增或更新 `evals/`
- 渲染层问题与研究纪律问题分开提交，避免 scope 混杂
- 对“未知项”要让它真正约束结论，而不是只在文中象征性提一句
- 把 final delivery cleanliness 当作硬门槛，而不是排版小瑕疵

---

## 相关文件入口

- `SKILL.md`：Agent 执行入口
- `ROUTING-MATRIX.md`：任务路由总表
- `ARCHITECTURE.md`：架构说明
- `SYSTEM-MAP.md`：系统地图
- `evals/README.md`：评估资产入口
- `scripts/render_pdf.py` / `scripts/md_to_pdf.py`：交付层脚本

---

## License

MIT
