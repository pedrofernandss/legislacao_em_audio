import re

def lowercase_text(original_text: str):
    return original_text.lower()

def replace_legal_terms(original_text: str):

    legal_patterns = [
        (r'(?i)(?<!\w)par\.?\s*?ún(?:ico)?\.?', 'parágrafo único'),
        (r'§§', 'parágrafos'),

        (r'§', 'parágrafo'),
        (r'(?i)(?<!\w)art\.?', 'artigo'),
        (r'(?i)(?<!\w)inc\.?', 'inciso'),
        (r'(?i)(?<!\w)al\.?', 'alínea'),
        (r'(?i)(?<!\w)caput', 'caput'),
        (r'(?i)(?<!\w)n[º°.]', 'número'),

        (r'(?m)^(\s*)([a-z])\)', r'\1alínea \2)')
    ]

    normalized_text = original_text

    for pattern, subs in legal_patterns:
        normalized_text = re.sub(pattern, subs, normalized_text)

    return normalized_text