#!/usr/bin/env bash
# validate-docs-structure.sh
# Property-based structural tests for documentation contracts
# Each contract tests a specific property of a documentation file.
# Exit 0 if all pass, 1 if any fail.
# Usage: bash scripts/validate-docs-structure.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAILED=0

pass() { echo "  ✅ $1"; }
fail() { echo "  ❌ $1"; FAILED=1; }

echo "=== Contract A: technical-analysis-discipline.md ==="
FILE_A="$ROOT/references/technical-analysis-discipline.md"

if grep -q -E "### [67]\. Definition-sensitive concepts" "$FILE_A" 2>/dev/null; then
  pass "A1: Has 'Definition-sensitive concepts' section"
else
  fail "A1: Missing Definition-sensitive concepts section"
fi

if grep -q -E "原始学术定义|academic definition|engineering definition|[Oo]perational definition|操作性定义" "$FILE_A" 2>/dev/null; then
  pass "A2: Contains definition-related terminology"
else
  fail "A2: Missing definition-related terminology"
fi

echo ""
echo "=== Contract B: report-template.md ==="
FILE_B="$ROOT/references/report-template.md"

if grep -q "| 概念 | 原始/严格定义 | 当代工程定义 | 本报告采用定义 | 排除边界 |" "$FILE_B" 2>/dev/null; then
  pass "B1: Has 5-column terminology boundary table"
else
  fail "B1: Missing terminology boundary table header"
fi

if grep -q "操作性定义" "$FILE_B" 2>/dev/null; then
  pass "B2: Contains operational definition template"
else
  fail "B2: Missing operational definition template"
fi

echo ""
echo "=== Contract C: technical-analysis-audit.md ==="
FILE_C="$ROOT/checklists/technical-analysis-audit.md"

if grep -q -E "定义敏感|definition-sensitive|概念边界|术语边界" "$FILE_C" 2>/dev/null; then
  pass "C1: Has definition-sensitive concept check"
else
  fail "C1: Missing definition-sensitive concept check"
fi

if grep -q -E "操作性定义|operational definition|工程范式" "$FILE_C" 2>/dev/null; then
  pass "C2: Has operational definition check"
else
  fail "C2: Missing operational definition check"
fi

echo ""
echo "=== Contract D: agentic-rag eval case ==="
FILE_D="$ROOT/evals/cases/agentic-rag-technical-deep-dive-compounded-case.md"

if grep -q -i "terminology\|术语\|definition.*boundary\|定义边界\|定义敏感\|概念定义" "$FILE_D" 2>/dev/null; then
  pass "D1: Has terminology/definition check in eval"
else
  fail "D1: Missing terminology/definition check in eval"
fi

echo ""
echo "=== Summary ==="
if [ "$FAILED" -eq 0 ]; then
  echo "  🟢 All contracts pass"
  exit 0
else
  echo "  🔴 Some contracts failed"
  exit 1
fi
