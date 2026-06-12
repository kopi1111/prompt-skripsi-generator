
# guardrails.py
# Simple automated checks for placeholders, PII, absolutes, and fabricated-citation patterns.
import re

PII_PATTERNS = [
    re.compile(r'\b\d{16}\b'),  # Indonesian NIK (approx)
    re.compile(r'\b\d{10,13}\b'),  # phone-ish numbers
    re.compile(r'[\w\.-]+@[\w\.-]+')  # emails
]

PLACEHOLDER_PATTERNS = [
    re.compile(r'\{\{.+?\}\}'),
    re.compile(r'\bTODO\b', re.IGNORECASE),
    re.compile(r'\[insert.+?\]', re.IGNORECASE)
]

ABSOLUTE_PHRASES = [
    "100%", "pasti", "selalu", "tidak pernah", "jaminan", "garansi", "sangat efektif", "terbukti"
]

CITATION_FABRIC_PATTERNS = [
    re.compile(r'\([A-Z][a-z]+, \d{4}\)'),  # (Author, 2020)
    re.compile(r'\bdoi:\d+\.\w+/\S+')
]

def run_guardrails_checks(text):
    issues = []
    # PII
    for p in PII_PATTERNS:
        if p.search(text):
            issues.append("PII detected")
            break
    # placeholders
    for p in PLACEHOLDER_PATTERNS:
        if p.search(text):
            issues.append("Placeholder token detected ({{}} or TODO)")
            break
    # absolutes
    for phrase in ABSOLUTE_PHRASES:
        if phrase in text.lower():
            issues.append("Absolute claim detected: '{}'".format(phrase))
            break
    # fabricated citation-like patterns
    for p in CITATION_FABRIC_PATTERNS:
        if p.search(text):
            issues.append("Citation-like pattern detected (avoid fabricated citations)")
            break
    # length checks (example)
    if len(text) < 50:
        issues.append("Output too short / might be incomplete")
    return issues
