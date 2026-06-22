#!/usr/bin/env python3
"""
Property-based contract validation for issue #329.

Verifies structural invariants for:
- Category Boundary (core/adjacent/excluded table, comparison unit)
- Participant Value-Chain Map (value capture, bottleneck, dependency, absorption risk)
- Demand Segmentation (>=2 dimensions, buyer, willingness-to-pay)
- Commercialization / Pricing (buyer, pricing unit, unit economics, validation metrics)
- Regulatory-to-Business transmission (business-variable linkage)
- Report-template additions (category boundary, demand segmentation, commercialization templates)
- Audit checklist additions (new check sections)

Usage:
    python tests/test_issue_329_contracts.py

Expected AFTER implementation: ALL PASS
"""

import re
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read(path):
    with open(os.path.join(REPO_ROOT, path), "r") as f:
        return f.read()

def file_exists(path):
    return os.path.isfile(os.path.join(REPO_ROOT, path))

def _section_text(content, heading_prefix):
    """Extract text under a specific ##-level heading until the next ## heading."""
    # Find all ##-level headings (not ###-level)
    lines = content.split('\n')
    in_section = False
    section_lines = []
    for line in lines:
        if line.startswith('## ') and not line.startswith('### '):
            if in_section:
                break  # hit next ## heading
            if heading_prefix.lower() in line.lower():
                in_section = True
                section_lines.append(line)
                continue
        if in_section:
            section_lines.append(line)
    return '\n'.join(section_lines)


# ═══════════════════════════════════════════════════════════════════
# C1: market-outlook-and-scenario-discipline.md — Category Boundary
# ═══════════════════════════════════════════════════════════════════

def test_c1a_category_boundary_section_exists():
    """C1a: reference doc contains Category Boundary section."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'Category Boundary|类别边界|市场定义与类别边界', content), \
        "Missing Category Boundary section"

def test_c1b_category_boundary_table_has_required_columns():
    """C1b: Category Boundary table includes core/adjacent/excluded + comparison unit."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    has_core = re.search(r'core\s*categor|核心市场|categories', content, re.IGNORECASE)
    has_adjacent = re.search(r'adjacent|邻接|相邻', content)
    has_excluded = re.search(r'excluded|排除|不纳入', content)
    has_comparison = re.search(r'comparison\s*unit|比较单位|不可直接比较', content)
    assert has_core and has_adjacent and has_excluded and has_comparison, \
        f"Category Boundary missing required concepts: core={bool(has_core)} adjacent={bool(has_adjacent)} excluded={bool(has_excluded)} comparison={bool(has_comparison)}"

def test_c1c_category_boundary_has_comparison_unit_rule():
    """C1c: Different categories must not be directly compared without explanation."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'不同类别.*不可直接比较|直接排名|统一比较单位|cross-category.*compar|across different categories', content), \
        "Missing cross-category comparison prohibition rule"

def test_c1d_category_boundary_has_participant_cross_layer_rule():
    """C1d: Rules for handling participants operating across multiple layers."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'跨层|cross.lay|按.*业务口径.*纳入|multiple.*layer|primary revenue', content), \
        "Missing cross-layer participant inclusion rule"


# ═══════════════════════════════════════════════════════════════════
# C2: market-outlook-and-scenario-discipline.md — Participant Value-Chain Map
# ═══════════════════════════════════════════════════════════════════

def test_c2a_participant_map_section_exists():
    """C2a: reference doc contains Participant Value-Chain Map section."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'Participant.*Value.Chain|参与者.*价值.*链|参与者地图', content), \
        "Missing Participant Value-Chain Map section"

def test_c2b_participant_map_has_value_capture():
    """C2b: Participant map includes value capture column or concept."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'value\s*capture|价值捕获|value\s*extraction|利润池', content), \
        "Missing value capture concept in participant map"

def test_c2c_participant_map_has_bottleneck():
    """C2c: Participant map includes bottleneck concept."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'bottleneck|瓶颈|约束环节', content), \
        "Missing bottleneck concept in participant map"

def test_c2d_participant_map_has_absorption_risk():
    """C2d: Participant map includes absorption risk or dependency concept."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'absorption\s*risk|absorbed.*risk|被吸收|dependency|依赖.*关系|取代风险', content), \
        "Missing absorption risk / dependency concept in participant map"


# ═══════════════════════════════════════════════════════════════════
# C3: market-outlook-and-scenario-discipline.md — Demand Segmentation
# ═══════════════════════════════════════════════════════════════════

def test_c3a_demand_segmentation_section_exists():
    """C3a: reference doc contains Demand Segmentation section."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'Demand\s*Segmentation|需求细分|需求分层', content), \
        "Missing Demand Segmentation section"

def test_c3b_at_least_two_segmentation_dimensions():
    """C3b: At least 2 segmentation dimensions specified."""
    section = _section_text(read("references/market-outlook-and-scenario-discipline.md"), "Demand Segmentation")
    assert section, "Demand Segmentation section not found"
    dimensions = re.findall(r'industry|行业|enterprise\s*size|企业规模|geograph|地域|数据主权|data\s*sovereignty|workload|workload类型|监管.*强度', section, re.IGNORECASE)
    assert len(set(dim.lower() for dim in dimensions)) >= 2, \
        f"Found fewer than 2 distinct segmentation dimensions in Demand Segmentation section: {len(set(dim.lower() for dim in dimensions))}"

def test_c3c_each_segment_has_job_and_buyer():
    """C3c: Each segment has job-to-be-done and buyer/payer identification."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    has_job = re.search(r'job.to.be.done|待完成工作|使用场景|use\s*case', content)
    has_buyer = re.search(r'buyer|购买者|payer|付费方|付费者|purchaser', content)
    assert has_job and has_buyer, \
        f"Segmentation missing job-to-be-done or buyer: job={bool(has_job)} buyer={bool(has_buyer)}"


# ═══════════════════════════════════════════════════════════════════
# C4: market-outlook-and-scenario-discipline.md — Commercialization / Pricing
# ═══════════════════════════════════════════════════════════════════

def test_c4a_commercialization_section_exists():
    """C4a: reference doc contains Commercialization / Pricing section."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'Commercialization|商业化|Pricing.*Layer|定价.*模式|商业模式', content), \
        "Missing Commercialization / Pricing section"

def test_c4b_commercialization_has_buyer_and_pricing_unit():
    """C4b: Commercialization section includes buyer and pricing unit."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    has_buyer = re.search(r'buyer|谁付费|付费方|谁在付钱', content)
    has_unit = re.search(r'pricing\s*unit|定价单位|按.*收费|per.query|per.token|per.seat|subscription|contract', content, re.IGNORECASE)
    assert has_buyer and has_unit, \
        f"Missing buyer or pricing unit in commercialization: buyer={bool(has_buyer)} unit={bool(has_unit)}"

def test_c4c_commercialization_has_unit_economics():
    """C4c: Commercialization includes unit economics variables."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'unit\s*econ|单位经济|gross\s*margin|毛利.*压力|margin.*pressure|成本结构', content), \
        "Missing unit economics / gross margin in commercialization"

def test_c4d_commercialization_has_validation_metrics():
    """C4d: Commercialization includes validation metrics (ARR, retention, etc.)."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'validation\s*metric|验证指标|ARR|retention|留存|付费.*mix|指标.*验证|关键.*商业.*指标', content), \
        "Missing validation metrics in commercialization"


# ═══════════════════════════════════════════════════════════════════
# C5: market-outlook-and-scenario-discipline.md — Regulatory-to-Business
# ═══════════════════════════════════════════════════════════════════

def test_c5a_regulatory_to_business_section_exists():
    """C5a: reference doc connects regulatory changes to business variables."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'regulatory.to.business|监管.*传导|监管.*商业|法规.*影响.*部署|regulation.*deployment|regulatory.*sales|cost of compliance|合规成本', content), \
        "Missing regulatory-to-business transmission section"

def test_c5b_regulatory_links_to_business_variables():
    """C5b: Regulatory section must link to specific business variables (not just list laws)."""
    section = _section_text(read("references/market-outlook-and-scenario-discipline.md"), "Regulatory")
    assert section, "Regulatory-to-Business Transmission section not found"
    business_vars = ['deployment', '部署', 'sales cycle', '销售周期', 'data residency', '数据驻留', 'content license', 'content licensing', '内容许可', 'gross margin', '毛利']
    hits = sum(1 for var in business_vars if re.search(var, section, re.IGNORECASE))
    assert hits >= 2, f"Regulatory section links to <2 business variables (found {hits})"

def test_c5c_commercial_numbers_have_role_labels():
    """C5c: Key commercial numbers have role labels and [Sxx] references."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    assert re.search(r'role\s*label|\[S\d+\]|数字.*角色|observed.*estimate.*scenario|角色标注', content), \
        "Missing requirement for commercial number role labeling"


# ═══════════════════════════════════════════════════════════════════
# C6: references/report-template.md — Template additions
# ═══════════════════════════════════════════════════════════════════

def test_c6a_report_template_has_category_boundary_template():
    """C6a: report-template.md contains category boundary table template."""
    content = read("references/report-template.md")
    assert re.search(r'Category\s*Boundary|类别边界|core.*adjacent.*excluded', content), \
        "report-template.md missing category boundary template"

def test_c6b_report_template_has_demand_segmentation_template():
    """C6b: report-template.md contains demand segmentation matrix template."""
    content = read("references/report-template.md")
    assert re.search(r'Demand\s*Segmentation|需求细分|segmentation.*matrix|segment.*dimension', content), \
        "report-template.md missing demand segmentation template"

def test_c6c_report_template_has_commercialization_memo():
    """C6c: report-template.md contains commercialization / pricing memo structure."""
    content = read("references/report-template.md")
    assert re.search(r'Commercialization|商业化|commercial.*memo|pricing.*structure|商业模式', content), \
        "report-template.md missing commercialization memo structure"


# ═══════════════════════════════════════════════════════════════════
# C7: checklists/market-outlook-audit.md — New audit sections
# ═══════════════════════════════════════════════════════════════════

def test_c7a_checklist_has_category_boundary_check():
    """C7a: market-outlook-audit.md contains category boundary check."""
    content = read("checklists/market-outlook-audit.md")
    assert re.search(r'Category\s*Boundary|类别边界|category.*boundary.*check|边界一致性', content, re.IGNORECASE), \
        "market-outlook-audit.md missing category boundary check"

def test_c7b_checklist_has_category_boundary_hard_fail():
    """C7b: Category boundary check has hard-fail or blocking gate."""
    content = read("checklists/market-outlook-audit.md")
    # hard-fail gate for missing category boundary declaration
    assert re.search(r'阻断|hard.fail|边界.*声明|category.*declaration|missing.*category', content, re.IGNORECASE), \
        "market-outlook-audit.md missing hard-fail for missing category boundary"

def test_c7c_checklist_has_demand_segmentation_check():
    """C7c: market-outlook-audit.md contains demand segmentation check."""
    content = read("checklists/market-outlook-audit.md")
    assert re.search(r'Demand\s*Segmentation|需求细分|segmentation.*check|需求分层', content, re.IGNORECASE), \
        "market-outlook-audit.md missing demand segmentation check"

def test_c7d_checklist_has_commercialization_check():
    """C7d: market-outlook-audit.md contains commercialization / pricing check."""
    content = read("checklists/market-outlook-audit.md")
    assert re.search(r'Commercialization|商业化|pricing.*check|商业闭环', content, re.IGNORECASE), \
        "market-outlook-audit.md missing commercialization check"

def test_c7e_checklist_has_regulatory_to_business_check():
    """C7e: market-outlook-audit.md contains regulatory-to-business transmission check."""
    content = read("checklists/market-outlook-audit.md")
    assert re.search(r'regulatory.to.business|监管.*传导|regulation.*business.*link', content, re.IGNORECASE), \
        "market-outlook-audit.md missing regulatory-to-business check"

def test_c7f_checklist_has_participant_map_check():
    """C7f: market-outlook-audit.md contains participant value-chain map check."""
    content = read("checklists/market-outlook-audit.md")
    assert re.search(r'Participant.*Map|参与者.*地图|participant.*value.chain|value.chain.*map', content, re.IGNORECASE), \
        "market-outlook-audit.md missing participant map check"


# ═══════════════════════════════════════════════════════════════════
# C8: Cross-file invariants
# ═══════════════════════════════════════════════════════════════════

def test_c8a_counterexample_exists():
    """C8a: At least one file contains the counterexample (category error example)."""
    for path in ["references/market-outlook-and-scenario-discipline.md", "references/report-template.md"]:
        content = read(path)
        if re.search(r'category\s*error|分类.*混乱|分类.*错误|术语定义.*存在.*但|反例|model.*API.*aggregator|OpenRouter.*DMXAPI', content, re.IGNORECASE):
            return  # found in at least one file
    assert False, "No counterexample / category-error example found in any reference file"

def test_c8b_commercial_numbers_role_label_requirement():
    """C8b: All numbers with role labels have [Sxx] reference requirement mentioned."""
    content = read("references/market-outlook-and-scenario-discipline.md")
    has_role_label = re.search(r'role\s*label|角色.*标注', content)
    has_sxx = re.search(r'\[S\d+\]', content)
    assert has_role_label and has_sxx, \
        f"Missing role label or [Sxx] requirement: role_label={bool(has_role_label)} sxx={bool(has_sxx)}"


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import inspect
    this_module = sys.modules[__name__]
    tests = [func for name, func in inspect.getmembers(this_module)
             if name.startswith("test_") and callable(func)]
    passed = 0
    failed = 0
    for test in sorted(tests, key=lambda t: t.__name__):
        try:
            test()
            print(f"  ✅ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"  Total: {passed + failed}  |  Passed: {passed}  |  Failed: {failed}")
    if failed:
        sys.exit(1)
