# Market Entry / Go-No-Go Report Template (route-specific)

**When to read:** only when the **market-entry** route (or a go/no-go /
constrained-choice task with entry logic) is selected (see the route's card in
`references/routes/market-entry.md`). The core default structure lives in
`references/report-template.md`; this file adds the go/no-go memo formatting
discipline and the input-boundary table.

## Market-entry / go-no-go memo formatting discipline

When the task is about market entry, regional expansion, country prioritization, or go/no-go judgment, do not format the report like a long regional backgrounder.

The page should help a decision-maker scan in this order:

1. recommendation
2. hard gates
3. shortlist / priority order
4. why the top path wins
5. what would change the decision

Formatting discipline for these cases:

- **Do not open with a dense paragraph summary.** Use short bullets or compact decision blocks.
- **Pull hard gates into their own block.** Do not bury budget, deployment, compliance, or localization gates inside long prose.
- **Use one visible comparison unit across countries.** Avoid free-form country notes as the primary structure.
- **Separate market roles visually when relevant:** regional hub, first revenue beachhead, later expansion market.
- **Keep country notes subordinate to the shortlist logic.** The report should feel like narrowing, not touring.
- **If milestones / KPIs / phased rollout are included, present them as a sequence block, not scattered commentary.**

Bad pattern:
- a long "市场分析" section followed by a recommendation paragraph at the end

Better pattern:
- recommendation block
- hard-gate block
- country shortlist table
- phased entry path
- change-the-decision conditions

### 输入边界与未指定项（constrained-choice / market-entry / market-outlook 建议）

对于 constrained-choice、provider-selection、market-entry、market-outlook 中涉及组织落地或方案选择的问题，建议在决策口径块（或等价位置）中包含以下输入边界表，明确哪些输入是已知的、哪些是假设的、哪些是未指定的。

**为什么需要：** 未经明确说明的"未指定项"如果隐含在结论中，会让读者误以为推荐适用于比实际更宽的场景。

| 边界维度 | 当前指定状态 | 说明 / 假设 / 未指定 |
|---------|-------------|---------------------|
| 组织规模/范围 | 已指定 / 未指定 | |
| 角色构成 | 已指定 / 未指定 | |
| 技术栈现状 | 已指定 / 未指定 | |
| 时间窗口 | 已指定 / 未指定 | |
| 合规/地域约束 | 已指定 / 未指定 | |
| 成本/预算基线 | 已指定 / 未指定 | |
| 优化目标 | 已指定 / 未指定 | |

**规则：**
- 未指定项必须转为显式假设（assumption），而非悄悄补全。
- 若未指定项的任何合理取值会导致结论翻转，该变量必须进入 uncertainty / sensitivity 分析。
- 该表不替代 Decision Scope 块中的排除项，而是补充说明"作者知道在省略什么"。
