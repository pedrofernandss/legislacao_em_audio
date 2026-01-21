import os
import re
from num2words import num2words

texto = """
## **RESOLUÇÃO Nº 17, DE 1989**

Aprova o Regimento Interno da Câmara dos Deputados.

A CÂMARA DOS DEPUTADOS, considerando a necessidade de adaptar o seu funcionamento e processo legislativo próprio à Constituição Federal,

## RESOLVE:

- Art. 1º O Regimento Interno da Câmara dos Deputados passa a vigorar na conformidade do texto anexo.
- Art. 2º Dentro de um ano a contar da promulgação desta resolução, a Mesa elaborará e submeterá à aprovação do Plenário o projeto de Regulamento Interno das Comissões e a alteração dos Regulamentos Administrativo e de Pessoal, para ajustá-los às diretrizes estabelecidas no Regimento.

*Parágrafo único.* Ficam mantidas as normas administrativas em vigor, no que não contrarie o anexo Regimento, e convalidados os atos praticados pela Mesa no período de 1º de fevereiro de 1987, data da instalação da Assembléia Nacional Constituinte, até o início da vigência desta resolução.

- Art. 3º A Mesa apresentará projeto de resolução sobre o Código de Ética e Decoro Parlamentar. *[\(Vide Resolução nº 25, de 2001\)](https://www2.camara.leg.br/legin/fed/rescad/2001/resolucaodacamaradosdeputados-25-10-outubro-2001-320496-publicacaooriginal-1-pl.html)*
- Art. 4º Ficam mantidas, até o final da sessão legislativa em curso, com seus atuais Presidente e Vice-Presidentes, as Comissões Permanentes criadas e organizadas na forma da Resolução nº 5, de 1989, que terão competência em relação às matérias das Comissões que lhes sejam correspondentes ou com as quais tenham maior afinidade, conforme discriminação constante do texto regimental anexo (art. 32). *[\(Vide Resolução nº 20, de 2004\)](https://www2.camara.leg.br/legin/fed/rescad/2004/resolucaodacamaradosdeputados-20-17-marco-2004-783666-publicacaooriginal-151140-pl.html)*
- § 1º Somente serão apreciadas conclusivamente pelas Comissões, na conformidade do art. 24, II, do novo Regimento, as proposições distribuídas a partir do início da vigência desta Resolução.
- § 2º Excetuam-se do prescrito no parágrafo anterior os projetos em trâmite na Casa, pertinentes ao cumprimento dos arts. 50 e 59 do Ato das Disposições Constitucionais Transitórias, em relação aos quais o Presidente da Câmara abrirá o prazo de cinco sessões para a apresentação de emendas nas Comissões incumbidas de examinar o mérito das referidas proposições.
- Art. 5º Ficam mantidas, até o final da legislatura em curso, as lideranças constituídas, na forma das disposições regimentais anteriores, até a data da promulgação do Regimento Interno.

"""

texto = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', texto)

texto = re.sub(r'^###\s+(.+)$', r'<break time="1s"/> \1 <break time="300ms"/>', texto, flags=re.MULTILINE)

texto = re.sub(r'^##\s+(.+)$', r'<break time="1500ms"/> \1 <break time="500ms"/>', texto, flags=re.MULTILINE)

texto = re.sub(r'^#\s+(.+)$', r'<break time="2s"/> \1 <break time="1s"/>', texto, flags=re.MULTILINE)

texto = re.sub(r'^-\s+(.+)$', r'<break time="500ms"/> \1', texto, flags=re.MULTILINE)

ssml_final = f"<speak>{texto}</speak>"

print(ssml_final)