# Eval: Provider Selection Enterprise Rollout Missing Case

**Verdict:** CONDITIONAL PASS (enterprise rollout layer missing)

**Route:** provider-selection

**Failure class:** structural-completeness — 推荐结构存在完整排名逻辑，但缺乏企业落地蓝图

## Goal

验证 provider-selection 报告在满足所有核心决策纪律（当前快照、追溯、排名、角色标签）的情况下，是否仍然会因为缺少企业落地蓝图（推荐层级、团队路线、TCO、迁移 checklist、未决问题关联）而降低对企业采购者的决策可用性。

## 场景

一份 provider-selection 报告，推荐了 Coding Agent 供应商选择。报告在以下方面表现良好：

- ✅ 当前供应商快照已核验最新模型/API 家族
- ✅ 7 列 Source Register + claim-level 内联引用 `[Sxx]`
- ✅ 数字角色标签（observed / proxy / assumption / model-output）
- ✅ 排序短名单：Top 1、Runner-up、淘汰项及原因
- ✅ 反转条件清晰
- ✅ 路由元数据和审计块正确

但报告**完全缺失**：

- ❌ 推荐层级——仅有数字评分排名，没有"首选 / 备选 / 次选 / 避免"分类
- ❌ 团队规模路线——没有区分小团队/中型/大型的不同实施路径
- ❌ 迁移 checklist——没有 inventory、安全评估、SSO 集成、pilot、培训、退出条件任何内容
- ❌ TCO——只有简单的 seat/API 单价比较，没有网络/合规/审计/培训/切换成本，没有边界声明
- ❌ 未决问题与推荐强度关联——大陆可访问性、签约主体不确定性没有影响推荐层级

## 期望

一个面向企业采购者的 provider-selection 报告，在完成核心排名逻辑后应附加以下内容：

1. **推荐层级表**（首选/备选/次选/避免），而不是只有总分排名
2. **团队规模实施路线**，至少覆盖小/中/大三种治理场景
3. **迁移 checklist**，覆盖 inventory、安全、身份、CI 集成、培训、试运行、退出
4. **TCO 模板**，含直接费+隐藏成本+边界声明+角色标签
5. **未决问题 → 推荐强度影响表**

## 当前报告检查结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 当前供应商快照 | ✅ | 已核验最新模型版本、定价、区域可达性 |
| Source Register 7 列 | ✅ | 完整 |
| Claim-level citation | ✅ | 每个关键 claim 有 `[Sxx]` |
| 数字角色标签 | ✅ | 评分/定价列有角色标识 |
| 排序短名单 | ✅ | Top 1、Runner-up、淘汰项 |
| 反转条件 | ✅ | 清晰 |
| **推荐层级** | ❌ | 只有 1-4 排名，无首选/备选/次选/避免 |
| **团队规模路线** | ❌ | 未提及 |
| **迁移 checklist** | ❌ | 未提供 |
| **TCO + 边界声明** | ❌ | 仅有 seat 单价，无 hidden cost |
| **未决问题 → 推荐强度** | ❌ | 可访问性问题无影响说明 |

## 规则/纪律引用

- `ROUTING-MATRIX.md` §Provider / Vendor Selection — Visible artifact contract
- `references/decision-report-template.md` §Provider-selection 企业落地蓝图（详见模板中加粗段落）
- `checklists/option-selection-final-audit.md` §Enterprise rollout gate
- `references/option-selection-and-shortlist-discipline.md` §When the task involves enterprise provider selection（详见启发式问题列表）

## 修复方向

在 provider-selection 输出中，当目标读者为企业/采购/治理团队时，在排名逻辑之后附加企业落地蓝图（推荐层级、团队路线、迁移 checklist、TCO、未决问题关联表）。
