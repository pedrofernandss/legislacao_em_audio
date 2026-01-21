from google.cloud import texttospeech

texto_ssml = f"""
<speak>
<break time="1500ms"/> **RESOLUÇÃO Nº 17, DE 1989** <break time="500ms"/>

Aprova o Regimento Interno da Câmara dos Deputados.

A CÂMARA DOS DEPUTADOS, considerando a necessidade de adaptar o seu funcionamento e processo legislativo próprio à Constituição Federal,

<break time="1500ms"/> RESOLVE: <break time="500ms"/>

<break time="500ms"/> Art. 1º O Regimento Interno da Câmara dos Deputados passa a vigorar na conformidade do texto anexo.
<break time="500ms"/> Art. 2º Dentro de um ano a contar da promulgação desta resolução, a Mesa elaborará e submeterá à aprovação do Plenário o projeto de Regulamento Interno das Comissões e a alteração dos Regulamentos Administrativo e de Pessoal, para ajustá-los às diretrizes estabelecidas no Regimento.

*Parágrafo único.* Ficam mantidas as normas administrativas em vigor, no que não contrarie o anexo Regimento, e convalidados os atos praticados pela Mesa no período de 1º de fevereiro de 1987, data da instalação da Assembléia Nacional Constituinte, até o início da vigência desta resolução.

<break time="500ms"/> Art. 3º A Mesa apresentará projeto de resolução sobre o Código de Ética e Decoro Parlamentar. *\(Vide Resolução nº 25, de 2001\)*
<break time="500ms"/> Art. 4º Ficam mantidas, até o final da sessão legislativa em curso, com seus atuais Presidente e Vice-Presidentes, as Comissões Permanentes criadas e organizadas na forma da Resolução nº 5, de 1989, que terão competência em relação às matérias das Comissões que lhes sejam correspondentes ou com as quais tenham maior afinidade, conforme discriminação constante do texto regimental anexo (art. 32). *\(Vide Resolução nº 20, de 2004\)*
<break time="500ms"/> § 1º Somente serão apreciadas conclusivamente pelas Comissões, na conformidade do art. 24, II, do novo Regimento, as proposições distribuídas a partir do início da vigência desta Resolução.
<break time="500ms"/> § 2º Excetuam-se do prescrito no parágrafo anterior os projetos em trâmite na Casa, pertinentes ao cumprimento dos arts. 50 e 59 do Ato das Disposições Constitucionais Transitórias, em relação aos quais o Presidente da Câmara abrirá o prazo de cinco sessões para a apresentação de emendas nas Comissões incumbidas de examinar o mérito das referidas proposições.
<break time="500ms"/> Art. 5º Ficam mantidas, até o final da legislatura em curso, as lideranças constituídas, na forma das disposições regimentais anteriores, até a data da promulgação do Regimento Interno.
</speak>
"""

client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(ssml=texto_ssml)

voice = texttospeech.VoiceSelectionParams(
    language_code = "pt-BR", 
    name="pt-BR-Chirp3-HD-Aoede",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("Audio content written to file 'output.mp3'")