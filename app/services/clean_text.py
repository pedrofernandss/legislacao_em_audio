import re

class CleanText:
    def __init__(self):

        self.ordinal_map = {
            "1" : "primeiro", "2": "segundo", "3": "terceiro",
            "4": "quarto", "5": "quinto", "6": "sexto",
            "7": "sétimo", "8": "oitavo", "9": "nono"
        }

    def _replace_ordinals(self, match):
        prefix = match.group(1)
        number = match.group(2)

        if number in self.ordinal_map:
            return f"{prefix} {self.ordinal_map[number]}"
        return f"{prefix} {number}"

    def expand_legal_terms(self, text: str) -> str:

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

        expanded_text = text

        for pattern, subs in legal_patterns:
            expanded_text = re.sub(pattern, subs, expanded_text)

        return expanded_text

    def remove_markdown_artifacts(self, text: str) -> str:
        patterns = [
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),
            (r'[*_#>{}]', '')
        ]

        clean = text
        for pat, sub in patterns:
            clean = re.sub(pat, sub, clean)

        return clean.strip()

    def clean(self, text: str) -> str:
        text = self.remove_markdown_artifacts(text)
        text = self.expand_legal_terms(text)

        return text