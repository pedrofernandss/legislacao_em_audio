import re
from num2words import num2words

texto = "Eu tenho 12 laranjas"
novo_texto = re.sub(r'\d+', lambda match: num2words(match.group(), lang='pt_BR'), texto)
print(novo_texto)

texto = "Art. 5° da constituição"
novo_text = re.sub(r'\d+°', lambda match: num2words(match.group()[:-1], lang='pt_BR', to='ordinal'), texto)
print(novo_text)