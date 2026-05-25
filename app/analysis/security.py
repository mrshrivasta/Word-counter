import re
import unicodedata

def analyze_security(text):
    if not text:
        return {}

    # 1. Invisible characters detection
    invisible_chars = re.findall(r'[\u200b-\u200d\ufeff\u00ad]', text)

    # 2. Unicode normalization/spoofing check (simplified)
    # Checking if text contains characters from multiple scripts which might indicate homoglyph attacks
    scripts = set()
    for char in text:
        name = unicodedata.name(char, "")
        script = name.split()[0] if name else ""
        if script:
            scripts.add(script)

    # 3. XSS / Script injection patterns
    xss_patterns = [
        r'<script.*?>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe.*?>',
        r'<img.*?onerror.*?>'
    ]
    xss_matches = []
    for pattern in xss_patterns:
        if re.search(pattern, text, re.I):
            xss_matches.append(pattern)

    # 4. Suspicious payloads (SQLi etc placeholders)
    sqli_patterns = [r"'.*?OR\s+.*?=.*?", r"--", r"/\*.*?\*/"]
    sqli_matches = [p for p in sqli_patterns if re.search(p, text, re.I)]

    return {
        'invisible_char_count': len(invisible_chars),
        'multi_script_detected': len(scripts) > 2,
        'scripts_used': list(scripts)[:5],
        'xss_risk_detected': len(xss_matches) > 0,
        'xss_patterns_found': xss_matches,
        'sqli_risk_detected': len(sqli_matches) > 0,
        'security_score': max(0, 100 - (len(invisible_chars) * 10) - (len(xss_matches) * 50))
    }
