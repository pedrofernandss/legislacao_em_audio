import re

def lowercase_text(original_text: str) -> str:
    return original_text.lower()

def replace_legal_terms(original_text: str) -> str:

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

def remove_special_char(original_text:str) -> str:

    characteres_to_remove = [

        (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),
        (r'[*_#>{}]', '')
    ]

    clean_text = original_text

    for char, subs in characteres_to_remove:
        clean_text = re.sub(char, subs, clean_text)

    return clean_text
