import re
from num2words import num2words

output = []
final = []
texto = "Eu tenho 12 laranjas"
lista_texto = texto.split(" ")
print(lista_texto)

for palavra in lista_texto:
    if palavra.isdigit():
        output.append(num2words(palavra, lang='pt_BR'))
    else:
        output.append(palavra)

final.append(' '.join(output))
print(final)

novo_texto = re.sub(r'\d+', lambda match: num2words(match.group(), lang='pt_BR'), texto)
print(novo_texto)

texto = "Art. 5° da constituição"
novo_text = re.sub(r'\d+°', lambda match: num2words(match.group()[:-1], lang='pt_BR', to='ordinal'), texto)
print(novo_text)