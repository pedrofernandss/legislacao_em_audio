from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(text = "Olá Luiza Fernandes, o que você acha desta voz para seus áudios?")

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