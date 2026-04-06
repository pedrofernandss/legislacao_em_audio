import os

from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

azure_sdk_key = os.getenv("AZURE_SPEECH_SKD_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")

speech_config = speechsdk.SpeechConfig(subscription=azure_sdk_key, endpoint=azure_endpoint)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name='pt-BR-ThalitaMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def generate_tts(text):

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    return speech_synthesis_result