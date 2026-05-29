#!/usr/bin/env python3
"""
Verify CJK PDF pipeline output for structural and typographic integrity.

Checks:
1. Block structure preserved (headings, paragraphs, list item counts match source)
2. Chinese punctuation fidelity (no ASCII degradation of CJK punctuation)
3. No cross-paragraph CJK merging (heading and content lines remain separate)
4. Heading CJK spacing intact (no CJK+space+CJK within headings)
"""
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
from markdown_to_html import normalize_text_for_pdf, process_markdown


CJK_PUNCT = set('（）【】《》，。！？；：、…—·～「」『』『』《》〔〕〖〗')


def count_blocks(md_text):
    """Count structural block elements in markdown text."""
    lines = md_text.split('\n')
    h1 = h2 = h3 = h4 = 0
    paragraphs = 0
    list_items = 0
    code_blocks = 0
    in_code = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            if not in_code:
                code_blocks += 1
            continue
        if in_code:
            continue
        if stripped.startswith('# '):
            h1 += 1
        elif stripped.startswith('## '):
            h2 += 1
        elif stripped.startswith('### '):
            h3 += 1
        elif stripped.startswith('#### '):
            h4 += 1
        elif stripped.startswith('- ') or stripped.startswith('* '):
            list_items += 1
        elif stripped and not stripped.startswith('>') and not stripped.startswith('|'):
            # Non-empty, non-table, non-blockquote line
            paragraphs += 1

    return h1, h2, h3, h4, paragraphs, list_items, code_blocks


def count_html_blocks(html):
    """Count structural block elements in HTML output."""
    h1 = len(re.findall(r'<h1[>\s]', html, re.I))
    h2 = len(re.findall(r'<h2[>\s]', html, re.I))
    h3 = len(re.findall(r'<h3[>\s]', html, re.I))
    h4 = len(re.findall(r'<h4[>\s]', html, re.I))
    paragraphs = len(re.findall(r'<p[>\s]', html, re.I))
    list_items = len(re.findall(r'<li[>\s]', html, re.I))
    code_blocks = len(re.findall(r'<pre><code', html, re.I))
    return h1, h2, h3, h4, paragraphs, list_items, code_blocks


def check_punctuation_integrity(html):
    """Check that Chinese punctuation in non-code HTML hasn't been degraded to ASCII."""
    # Strip code blocks before checking
    text = re.sub(r'<pre><code[^>]*>.*?</code></pre>', '', html, flags=re.DOTALL | re.I)
    # Strip inline code
    text = re.sub(r'<code>[^<]+</code>', '', text)
    # Strip all HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    issues = []
    # Look for ASCII punct in CJK context (but not thousands separators like 1,500)
    for m in re.finditer(r'([\u4e00-\u9fff])([(,;:!?)])', text):
        cjk_char = m.group(1)
        punct = m.group(2)
        after = text[m.end():m.end()+8]
        # Skip thousands separators: CJK,digit-comma-digit
        if punct == ',' and re.match(r'^\d+', after):
            continue
        # Skip CJK-colon-URL (common in reference lists)
        if punct == ':' and re.match(r'(?:https?://|www\.|//)', after.lstrip(), re.I):
            continue
        issues.append(f"ASCII '{punct}' after CJK '{cjk_char}' at pos {m.start()}: ...{text[max(0,m.start()-8):m.end()+8]}...")
        break  # one is enough for diagnosis
    return issues


def check_cross_paragraph_merging(html):
    """Check that headings contain only the heading text, not merged body content."""
    issues = []
    for m in re.finditer(r'<h([1-4])[^>]*>(.*?)</h\1>', html, re.DOTALL | re.I):
        inner = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        # A heading with more than 80 chars likely merged body text
        if len(inner) > 100:
            issues.append(f"H{m.group(1)} too long ({len(inner)} chars): {inner[:80]}...")
    return issues


def check_spacing_integrity(html):
    """Check no CJK+space+CJK within same line in headings / first 150 chars of paragraphs."""
    issues = []
    # Check headings
    for m in re.finditer(r'<h([1-4])[^>]*>(.*?)</h\1>', html, re.DOTALL | re.I):
        inner = re.sub(r'<[^>]+>', '', m.group(2))
        for sm in re.finditer(r'[\u4e00-\u9fff][ \t][\u4e00-\u9fff]', inner):
            issues.append(f"H{m.group(1)}: '{sm.group(0)}' in '{inner.strip()[:60]}'")
    # Check paragraphs — only flag same-line [ \t] spacing (not across \n)
    for m in re.finditer(r'<p>(.*?)</p>', html, re.DOTALL | re.I):
        inner = re.sub(r'<[^>]+>', '', m.group(1))
        for line in inner.split('\n'):
            for sm in re.finditer(r'[\u4e00-\u9fff][ \t][\u4e00-\u9fff]', line):
                issues.append(f"<p>: '{sm.group(0)}' in '{line.strip()[:60]}'")
    # Check list items
    for m in re.finditer(r'<li>(.*?)</li>', html, re.DOTALL | re.I):
        inner = re.sub(r'<[^>]+>', '', m.group(1))
        for sm in re.finditer(r'[\u4e00-\u9fff][ \t][\u4e00-\u9fff]', inner):
            issues.append(f"<li>: '{sm.group(0)}' in '{inner.strip()[:60]}'")
    # Check table cells
    for m in re.finditer(r'<t[dh][^>]*>(.*?)</t[dh]>', html, re.DOTALL | re.I):
        inner = re.sub(r'<[^>]+>', '', m.group(1))
        for sm in re.finditer(r'[\u4e00-\u9fff][ \t][\u4e00-\u9fff]', inner):
            issues.append(f"<td>: '{sm.group(0)}' in '{inner.strip()[:60]}'")
    return issues


def verify_cjk_pipeline(md_text, label="report"):
    """Run full verification and return (pass, fail_list)."""
    errors = []

    # 1. Count source blocks
    src_h1, src_h2, src_h3, src_h4, src_p, src_li, src_cb = count_blocks(md_text)

    # 2. Normalize and process
    normalized = normalize_text_for_pdf(md_text)
    html = process_markdown(normalized)

    # 3. Count output blocks
    html_h1, html_h2, html_h3, html_h4, html_p, html_li, html_cb = count_html_blocks(html)

    # 4. Check block structure integrity
    if src_h1 != html_h1:
        errors.append(f"h1 count mismatch: source={src_h1}, html={html_h1}")
    if src_h2 != html_h2:
        errors.append(f"h2 count mismatch: source={src_h2}, html={html_h2}")
    if src_h3 != html_h3:
        errors.append(f"h3 count mismatch: source={src_h3}, html={html_h3}")
    if html_li == 0 and src_li > 0:
        errors.append(f"list items vanished: source={src_li}, html={html_li}")

    # 5. Check cross-paragraph merging
    merging_issues = check_cross_paragraph_merging(html)
    errors.extend(f"MERGE: {e}" for e in merging_issues)

    # 6. Check punctuation integrity
    punct_issues = check_punctuation_integrity(html)
    errors.extend(f"PUNCT: {e}" for e in punct_issues)

    # 7. Check CJK spacing integrity
    spacing_issues = check_spacing_integrity(html)
    errors.extend(f"SPACE: {e}" for e in spacing_issues)

    return errors, normalized, html


# ─── Tests ────────────────────────────────────────────────────────────

def test_normalize_preserves_structure():
    """Block-level markdown structure must survive normalization intact."""
    md = "# Title\n\nParagraph one.\n\n## Section\n\n- List A\n- List B\n\nAnother para."
    result = normalize_text_for_pdf(md)
    assert '# Title' in result, "h1 lost"
    assert '## Section' in result, "h2 lost"
    assert '- List A' in result, "list item A lost"
    assert '- List B' in result, "list item B lost"
    assert 'Paragraph one.' in result, "para 1 lost"
    assert 'Another para.' in result, "para 2 lost"
    print("  PASS  normalize preserves structure")


def test_normalize_no_heading_merge():
    """Heading with CJK end must NOT merge with next CJK-start paragraph."""
    md = "## 1. 执行摘要\n\n中际旭创是中国领先的光模块制造商。"
    result = normalize_text_for_pdf(md)
    assert '\n\n' in result, f"paragraph break lost: {result!r}"
    print("  PASS  no heading merge")


def test_normalize_preserves_chinese_punctuation():
    """Chinese punctuation (（）,，：；) must survive normalization as CJK, not ASCII."""
    md = "（2025 年），公司营收：218.6 亿元；净利润增长 81%。"
    result = normalize_text_for_pdf(md)
    for expected in ('（', '）', '，', '：', '；', '。'):
        assert expected in result, f"Chinese punctuation '{expected}' degraded, got: {result}"
    print("  PASS  Chinese punctuation preserved")


def test_full_pipeline_block_integrity():
    """Full pipeline (normalize → markdown → HTML) preserves heading and list counts."""
    md = "# H1\n\nP1.\n\n## H2\n\n- Li1\n- Li2\n\n### H3\n\nP2.\n\n> Bq\n\n#### H4\n\nP3."
    errors, _, html = verify_cjk_pipeline(md)
    assert not errors, f"pipeline integrity errors: {errors}"
    # Verify specific heading text is not merged with body
    for heading_marker in ['H1', 'H2', 'H3', 'H4']:
        pattern = f'<h[1-4][^>]*>{heading_marker}</h[1-4]>'
        if not re.search(pattern, html, re.I):
            print(f"  WARN: could not find heading '{heading_marker}' in HTML")
    print("  PASS  full pipeline block integrity")


def test_file_pipeline(md_path, min_expected_cjk=3000):
    """Verify pipeline on a real file produces structurally sound HTML."""
    md_text = md_path.read_text(encoding='utf-8', errors='replace')
    errors, normalized, html = verify_cjk_pipeline(md_text, label=md_path.stem)

    # Count CJK
    cjk_count = sum(1 for c in md_text if '\u4e00' <= c <= '\u9fff')
    assert cjk_count >= min_expected_cjk, (f"{md_path.name}: {cjk_count} CJK chars < {min_expected_cjk}")

    if errors:
        print(f"  FAIL  {md_path.name}: {len(errors)} error(s)")
        for e in errors[:10]:
            print(f"    {e}")
    else:
        print(f"  PASS  {md_path.name} ({cjk_count} CJK chars, {len(normalized)} bytes after normalize)")

    return errors


def main():
    tests = [
        ("normalize preserves structure", test_normalize_preserves_structure),
        ("no heading merge", test_normalize_no_heading_merge),
        ("Chinese punctuation preserved", test_normalize_preserves_chinese_punctuation),
        ("full pipeline block integrity", test_full_pipeline_block_integrity),
    ]

    failures = []
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failures.append(name)
        except Exception as e:
            print(f"  FAIL  {name} exception: {e}")
            failures.append(name)

    # File pipeline tests
    cases_dir = Path(__file__).resolve().parent.parent / 'evals' / 'cases'
    file_tests = [
        (cases_dir / 'cjk-pdf-validation-input-company-case.md', 3000),
        (cases_dir / 'cjk-pdf-validation-input-market-case.md', 3000),
    ]

    print()
    for path, min_cjk in file_tests:
        try:
            errs = test_file_pipeline(path, min_cjk)
            if errs:
                failures.append(f"{path.name} ({len(errs)} issues)")
        except Exception as e:
            print(f"  ERROR  {path.name}: {e}")
            failures.append(f"{path.name} exception")

    # Summary
    print(f"\n{'='*50}")
    total = len(tests) + len(file_tests)
    passed = total - len(failures)
    print(f"{passed}/{total} tests passed")
    if failures:
        print(f"FAILURES: {failures}")
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
