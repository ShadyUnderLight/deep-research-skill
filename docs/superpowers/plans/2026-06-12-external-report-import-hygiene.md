# External Deep-Research Import Hygiene — Implementation Plan

> **For agentic workers:** Use subagent-driven-development (recommended) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add import hygiene rules to prevent GPT/Claude/Gemini internal citations (`turn...`, `sandbox:`, `\ue000cite`) from entering deliverable Markdown.

**Architecture:** Three layers — (1) reference doc defines the rule, (2) checklists enforce it at audit time, (3) optional validator script provides automated scanning. All additions are additive (no existing logic changed).

**Tech Stack:** Python 3.10+ for validator script, Markdown for documentation/checklists

**Type Contracts (SDD):**

```
// ── Data types for external citation hygiene ──

// Patterns that MUST NOT appear in deliverable body text:
//   - \ue000cite — GPT internal citation placeholder (unicode private use area)
//   - sandbox:    — GPT sandbox file path prefix
//   - turn\d+(?:view|search|source)? — GPT session turn reference

ExternalCitationPattern = Literal["cite", "sandbox", "turn"]

ExternalCitationMatch = {
  pattern: ExternalCitationPattern,
  match_text: str,
  line_number: int,
  context: str,  // surrounding line for context
}

// Hygiene check result
HygieneCheckResult = {
  passed: bool,
  matches: list[ExternalCitationMatch],
  severity: "warning"   // always warning, never hard-fail
}

// Contract: check_external_citation_hygiene(text: str) -> HygieneCheckResult
//   - Scans body text (excluding fenced code blocks) for external citation patterns
//   - Returns all matches with line numbers
//   - Never raises exceptions
//   - purity: pure function (no side effects)
```

---

### Task 1: Reference doc — External research import hygiene section

**Files:**
- Modify: `references/source-traceability-and-claim-citation.md` (after line 63, §What does NOT qualify)

**Spec:**
- Add a new `## External research output / Imported report hygiene` subsection
- Content per issue #263: define hygiene rules for `turn...` / `\ue000cite...` / `sandbox:` / temp file IDs
- Must state: external research outputs may inform structure and judgment, but internal citation handles and sandbox assets are not valid final-report citations or assets
- Must require: every external citation must be resolved to a real URL/DOI before delivery, or removed
- Must require: sandbox images must be regenerated as repo-accessible files or replaced with data tables

- [ ] **Step 1: Write the failing test (documentation gap check)**

  Non-code task — verify the current file lacks the required content:

  Run: `grep -c "Imported report hygiene" references/source-traceability-and-claim-citation.md`
  Expected: 0 (not present yet)

- [ ] **Step 2: Add "External research output / Imported report hygiene" section**

  Insert after the "What does NOT qualify as equivalent" section (after line 63, before the `### Shared-Workflow route coverage` section). Add:

  ```
  ## External research output / Imported report hygiene

  When importing or adapting output from external deep-research systems (GPT Deep Research, Claude, Gemini, etc.) as input material:

  ### Citation hygiene

  External deep-research systems often use internal citation handles that are not resolvable outside the originating session:

  - `turn...` IDs (`turn43view0`, `turn12source1`) are session-internal references — readers cannot open them
  - `\ue000cite...` placeholders are GPT-specific rendering artifacts with no meaning outside the chat
  - Temporary file IDs (`file-xxxxxxxxxxxx`) are session-scoped and expire

  **Rule:** These are NOT valid final-report citations. Before delivery, every external citation handle must be:
  1. Resolved into a real URL / DOI / file path and entered into the Source Register, OR
  2. Removed from the claim

  Example:
  
  - ❌ `MTT S5000 is the current flagship [\ue000cite\turn43view0]`
  - ✅ `MTT S5000 is positioned as the current flagship AI chip [S01]` (with S01 in Source Register)

  ### Asset hygiene

  External deep-research outputs may embed chart images from temporary sandbox paths:

  - `sandbox:/mnt/data/...` — GPT sandbox path, unreachable after session ends
  - `file-service://...` or similar ephemeral URIs

  **Rule:** Temporary sandbox image paths are NOT valid final-report assets. Charts or images must be:
  1. Regenerated into repository/vault-accessible files with source attribution, OR
  2. Replaced with the underlying data table and generation instructions

  ### What IS allowed

  External deep-research outputs may be used as comparison material, structural inspiration, or discovery input. Their:
  - analytical structure and judgment framework
  - dimension design and evaluation criteria
  - choice of comparison scope and methodology

  ...are all reusable. Only the internal citation handles and ephemeral asset paths are excluded. If the external report references a real, independently accessible URL or DOI, that is a valid candidate source — treat it like any other source in the Source Register.

  ### Relationship to existing rules

  These hygiene rules supplement the existing traceability discipline:
  - Source Register requirements (see §Structured Source Register Template) still apply
  - Format equivalence exemptions (see §Format equivalence exemption) still apply — `(Author, Year)` or `据 FY2025 年报` are valid even in imported content
  - The `DISCOVERY` source type restriction (see §Source type classification) still applies: search-level output is not a register entry
  ```

- [ ] **Step 3: Verify insertion is correct**

  Run: `grep -c "Imported report hygiene" references/source-traceability-and-claim-citation.md`
  Expected: 1

  Run: `grep -c "turn43view0" references/source-traceability-and-claim-citation.md`
  Expected: 1

- [ ] **Step 4: Commit**

  ```bash
  git add references/source-traceability-and-claim-citation.md
  git commit -m "docs(source-traceability): add external research import hygiene section"
  ```

---

### Task 2: final-audit checklist — Add delivery cleanliness check

**Files:**
- Modify: `checklists/final-audit.md` (after line 288, Delivery cleanliness section)

**Spec:**
- Add a new check item right after "presentation credibility leaks" check (line 288)
- Check must explicitly mention `turn...`, `\ue000cite`, `sandbox:`, and temporary file IDs

- [ ] **Step 1: Verify current state**

  Run: `grep "turn" checklists/final-audit.md`
  Expected: no match

- [ ] **Step 2: Add check item to Delivery cleanliness section**

  Insert after line 288 (the last item before "Quality bar" section). Add:

  ```
  - [ ] final report contains no external deep-research internal citation artifacts: no `turn\d+` session references, no `\ue000cite` placeholders, no `sandbox:` or temporary `file-` paths that are unreachable outside the source session; if such content exists, it must have been resolved into real sources / local assets (see `references/source-traceability-and-claim-citation.md` §External research output / Imported report hygiene)
  ```

- [ ] **Step 3: Verify insertion**

  Run: `grep "turn" checklists/final-audit.md`
  Expected: match found

- [ ] **Step 4: Commit**

  ```bash
  git add checklists/final-audit.md
  git commit -m "docs(final-audit): add external citation hygiene check to delivery cleanliness"
  ```

---

### Task 3: source-traceability checklist — Add hard-fail rules

**Files:**
- Modify: `checklists/source-traceability.md` (after line 18, in the hard-fail gate section)

**Spec:**
- Add a new hard-fail condition: body text contains `turn\d+` references, `\ue000cite` placeholders, or `sandbox:` image paths and they are NOT converted to real sources / local assets
- This is a new bullet under the existing hard-fail gate block

- [ ] **Step 1: Verify current state**

  Run: `grep -c "turn" checklists/source-traceability.md`
  Expected: 0

- [ ] **Step 2: Add hard-fail condition**

  After line 18 (the `- 例外：等效格式...` line), before the blank line and `- [ ] **conditional pass**` line, add:

  ```
  - [ ] **hard-fail gate（阻断级）**: 正文存在不可解析的外部深度研究报告引用——`turn\d+` 会话引用、`\ue000cite` 占位符、`sandbox:` 图片路径或临时 `file-` 路径——且未转换为可复核来源或本地资产（等效格式不适用于此规则——`turn43view0` 无论搭配何种 register 格式都不是可追溯引用）；任一违规 → **不可交付**
  ```

- [ ] **Step 3: Verify insertion**

  Run: `grep -c "turn" checklists/source-traceability.md`
  Expected: 1

- [ ] **Step 4: Commit**

  ```bash
  git add checklists/source-traceability.md
  git commit -m "docs(source-traceability): add hard-fail for external research citation artifacts"
  ```

---

### Task 4: Validator — Add external citation hygiene scanner

**Files:**
- Modify: `scripts/validate_report_quality.py`
- Test: `scripts/test_report_quality_validator.py`

**Spec:**
- Add pure function `check_external_citation_hygiene(cleaned: str) -> list[str]`
- Scan for three patterns after stripping fenced code blocks:
  1. `sandbox:` — GPT sandbox paths
  2. `turn\d+(?:view|source|search)?` — session turn references (must use word boundary to avoid matching "turnaround")
  3. `\ue000` or explicit `\ue000cite` — GPT cite placeholders
- Return warnings (never hard-fail) — one per unique match type found
- Integration: call from `validate_file()`, add warnings to the warnings list

**Property-based contracts:**
```
// Property 1: Empty text → no warnings
prop("empty text produces no warnings", lambda text="":
    len(check_external_citation_hygiene(text)) == 0)

// Property 2: Clean text → no false positives
prop("normal text produces no warnings", lambda text="据 FY2025 年报，公司营收增长 [S01]":
    len(check_external_citation_hygiene(text)) == 0)

// Property 3: Words like "turnaround" or "turning" → no false positives
prop("common English words with 'turn' prefix do not trigger",
    lambda text="The company is turning around its business model":
    len(check_external_citation_hygiene(text)) == 0)

// Property 4: Each pattern produces exactly 1 warning
prop("sandbox: path produces 1 warning", lambda text="![chart](sandbox:/mnt/data/foo.png)":
    len(check_external_citation_hygiene(text)) == 1)

prop("turn reference produces 1 warning", lambda text="as stated [turn43view0]":
    len(check_external_citation_hygiene(text)) == 1)

prop("cite placeholder produces 1 warning", lambda text="result \ue000cite\turn43view0":
    len(check_external_citation_hygiene(text)) >= 1)

// Property 5: Multiple pattern types → multiple warnings
prop("multiple pattern types produce multiple warnings",
    lambda text="[sandbox:/path] and [turn12view0] and \ue000cite":
    len(check_external_citation_hygiene(text)) >= 1)
    // Note: depends on whether patterns hit the same match
```

- [ ] **Step 1: Read current validator source**

  Review `scripts/validate_report_quality.py` lines 858-911 (the `validate_file` function) to understand how warnings are collected and printed.

- [ ] **Step 2: Write property-based test (TDD — RED)**

  Add to `scripts/test_report_quality_validator.py`. Create a new test group:

  ```python
  def test_external_hygiene_sandbox_warns() -> None:
      """sandbox: path should produce a warning (not hard-fail)."""
      text = """\
  ## Route and audit status

  **Primary route**: Provider / Vendor Selection

  | Audit | Status | 证据 |
  |-------|--------|------|
  | source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
  | final-audit | ✅ Passed | §2 各关卡可追溯 |

  ## Findings

  The chart shows revenue growth.

  ![revenue](sandbox:/mnt/data/revenue.png)

  ## Source Register

  | ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
  |----|-------------|-------------|------|---------|-------------|------------------|
  | S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
  """
      result = run_validator(text)
      # Must pass (exit 0) because hygiene is warning-level only
      assert result.returncode == 0, (
          f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
      )
      assert "external citation" in result.stdout.lower() or "sandbox" in result.stdout.lower(), (
          f"expected warning about sandbox in:\n{result.stdout}"
      )
      print("  PASS  external hygiene sandbox warns")

  def test_external_hygiene_turn_ref_warns() -> None:
      """turn reference should produce a warning (not hard-fail)."""
      text = """\
  ## Route and audit status

  **Primary route**: Provider / Vendor Selection

  | Audit | Status | 证据 |
  |-------|--------|------|
  | source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
  | final-audit | ✅ Passed | §2 各关卡可追溯 |

  ## Findings

  The report states that revenue grew 35% [\ue000cite\turn43view0].

  ## Source Register

  | ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
  |----|-------------|-------------|------|---------|-------------|------------------|
  | S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
  """
      result = run_validator(text)
      assert result.returncode == 0, (
          f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
      )
      assert "external citation" in result.stdout.lower() or "turn" in result.stdout.lower(), (
          f"expected warning about turn reference in:\n{result.stdout}"
      )
      print("  PASS  external hygiene turn ref warns")

  def test_external_hygiene_clean_passes() -> None:
      """Clean text (no external citation patterns) should pass without warnings."""
      text = """\
  ## Route and audit status

  **Primary route**: Provider / Vendor Selection

  | Audit | Status | 证据 |
  |-------|--------|------|
  | source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
  | final-audit | ✅ Passed | §2 各关卡可追溯 |

  ## Findings

  The company reported revenue of 7.02 billion RMB [S01].

  ## Source Register

  | ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
  |----|-------------|-------------|------|---------|-------------|------------------|
  | S01 | Annual Report FY2025 | primary | 2026-03-15 | https://example.com | high | §2 |
  """
      result = run_validator(text)
      assert result.returncode == 0, (
          f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
      )
      assert "external citation" not in result.stdout.lower(), (
          f"unexpected warning in:\n{result.stdout}"
      )
      print("  PASS  external hygiene clean passes")

  def test_external_hygiene_turnaround_no_false_positive() -> None:
      """Common word 'turnaround' should NOT trigger a false positive."""
      text = """\
  ## Route and audit status

  **Primary route**: Provider / Vendor Selection

  | Audit | Status | 证据 |
  |-------|--------|------|
  | source-traceability | ✅ Passed | §3 正文使用 [S01] 引用 |
  | final-audit | ✅ Passed | §2 各关卡可追溯 |

  ## Findings

  The company is executing a successful turnaround strategy [S01].

  ## Source Register

  | ID | Source Name | Source Type | Date | DOI/URL | Reliability | Claims Supported |
  |----|-------------|-------------|------|---------|-------------|------------------|
  | S01 | Example | secondary | 2026-01-01 | https://example.com | medium | §2 |
  """
      result = run_validator(text)
      assert result.returncode == 0, (
          f"expected pass, got {result.returncode}\nstdout: {result.stdout}"
      )
      assert "external citation" not in result.stdout.lower(), (
          f"unexpected warning about 'turnaround' in:\n{result.stdout}"
      )
      print("  PASS  external hygiene turnaround no false positive")
  ```

- [ ] **Step 3: Run tests — they should fail (RED)**

  Run: `python scripts/test_report_quality_validator.py`
  Expected: 4 new tests FAIL (function `check_external_citation_hygiene` not found yet)

- [ ] **Step 4: Implement scanner function**

  Add to `scripts/validate_report_quality.py`. Insert after the existing check functions (before `validate_file`):

  ```python
  # ── External citation hygiene checks ──────────────────────────────────

  EXTERNAL_CITE_SANDBOX_RE = re.compile(r"sandbox:/")
  EXTERNAL_CITE_TURN_RE = re.compile(r"\bturn\d+(?:view|source|search)?\b")
  EXTERNAL_CITE_UNICODE_RE = re.compile(r"[\ue000\ue001]cite")

  def check_external_citation_hygiene(cleaned: str) -> list[str]:
      """Scan for external deep-research internal citation artifacts.
      
      Checks for three categories of import hygiene violations:
      1. sandbox: paths — GPT sandbox file paths
      2. turn\d+ references — GPT session turn citations
      3. \ue000cite placeholders — GPT citation rendering artifacts
      
      These patterns bypass the project's source traceability discipline
      because they are not resolvable outside the originating session.
      
      Returns warnings only (never hard-fail), one per unique match type.
      """
      warnings: list[str] = []
      
      if EXTERNAL_CITE_SANDBOX_RE.search(cleaned):
          warnings.append(
              "External citation hygiene: body text contains 'sandbox:' path(s) — "
              "these are unreachable outside GPT session; convert to local assets "
              "or remove before delivery"
          )
      
      if EXTERNAL_CITE_TURN_RE.search(cleaned):
          warnings.append(
              "External citation hygiene: body text contains 'turnNxxx' reference(s) — "
              "these are GPT session-internal citations not resolvable by readers; "
              "resolve to real URL/DOI or remove before delivery"
          )
      
      if EXTERNAL_CITE_UNICODE_RE.search(cleaned):
          warnings.append(
              "External citation hygiene: body text contains \\ue000cite placeholder(s) — "
              "these are GPT-specific rendering artifacts; resolve to real URL/DOI or "
              "remove before delivery"
          )
      
      return warnings
  ```

- [ ] **Step 5: Integrate into validate_file**

  In the `validate_file()` function, after the existing warnings from `check_source_register_doi_coverage` (around line 880), add:

  ```python
      # 5. External citation hygiene (warnings only)
      warnings.extend(check_external_citation_hygiene(cleaned))
  ```

  Also renumber the subsequent comment numbers (6. → 7., etc.)

- [ ] **Step 6: Run validator tests — should pass (GREEN)**

  Run: `python scripts/test_report_quality_validator.py`
  Expected: all existing tests pass + 4 new tests pass

- [ ] **Step 7: Run a quick smoke test on a real report**

  Run: `python scripts/validate_report_quality.py 光模块行业竞争格局研究报告.md`
  Expected: passes without external citation warnings

- [ ] **Step 8: Commit**

  ```bash
  git add scripts/validate_report_quality.py scripts/test_report_quality_validator.py
  git commit -m "feat(validator): add external citation hygiene scanner"
  ```

---

### Task 5: Self-review / Reflexion

- [ ] **Step 1: Verify all changes are consistent**

  Run: `git log --oneline -5`
  Verify each commit message matches the task.

- [ ] **Step 2: Verify checklist and reference cross-references**

  Run: `grep "references/source-traceability-and-claim-citation.md" checklists/final-audit.md`
  Expected: cross-reference to §External research output / Imported report hygiene

  Run: `grep "references/source-traceability-and-claim-citation.md" checklists/source-traceability.md`
  Expected: cross-reference present or at minimum consistent language

- [ ] **Step 3: Verify no false positive risk**

  Run: `python -c "
import re
# Test the regexes against common false-positive scenarios
sandbox_re = re.compile(r'sandbox:')
turn_re = re.compile(r'\bturn\d+(?:view|source|search)?\b')
cite_re = re.compile(r'[\ue000\ue001]cite')
assert not sandbox_re.search('The sandbox environment is configured')
assert not turn_re.search('The company turnaround strategy')
assert not turn_re.search('The turning point')
assert not turn_re.search('A return to growth')
assert turn_re.search('see turn43view0')
assert sandbox_re.search('![img](sandbox:/mnt/data/x.png)')
print('All false-positive guards verified OK')
"`

- [ ] **Step 4: Full test regression**

  Run: `python scripts/test_report_quality_validator.py`
  Expected: All tests pass

- [ ] **Step 5: Commit remaining**

  ```bash
  git add -A
  git commit -m "reflexion: verify external citation hygiene — all tests pass, no false positives"
  ```

- [ ] **Step 6: Open PR**

  ```bash
  git push origin HEAD
  gh pr create --fill
  ```

---

### Rollback plan

If any step fails:
- `git reset --hard HEAD` to undo uncommitted changes
- `git rebase --abort` if in rebase
- Individual file revert: `git checkout HEAD -- <file>` before committing
- Commit revert: `git revert <sha>` for committed changes
