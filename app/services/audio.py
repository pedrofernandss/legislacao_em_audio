import os
from pathlib import Path

from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

DEFAULT_VOICE = "pt-BR-ThalitaMultilingualNeural"


def _resolve_subscription() -> str:
    subscription = os.getenv("AZURE_SPEECH_KEY") or os.getenv("AZURE_SPEECH_SKD_KEY")
    if not subscription:
        raise RuntimeError("Missing Azure speech key. Set AZURE_SPEECH_KEY or AZURE_SPEECH_SKD_KEY.")
    return subscription


def _build_speech_config() -> speechsdk.SpeechConfig:
    subscription = _resolve_subscription()
    endpoint = os.getenv("AZURE_ENDPOINT")
    region = os.getenv("AZURE_SPEECH_REGION")

    if endpoint:
        speech_config = speechsdk.SpeechConfig(subscription=subscription, endpoint=endpoint)
    elif region:
        speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)
    else:
        raise RuntimeError("Missing Azure speech region or endpoint. Set AZURE_SPEECH_REGION or AZURE_ENDPOINT.")

    speech_config.speech_synthesis_voice_name = os.getenv("AZURE_SPEECH_VOICE", DEFAULT_VOICE)
    return speech_config


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_ssml(tagged_text: str, voice: str, rate: str | None = None) -> str:
    """Wrap already-escaped, break-tagged text in a valid SSML <speak> document.

    `tagged_text` must already be XML-escaped and must have had its <break>
    tags inserted AFTER escaping (see Text.insert_speech_breaks) — this function
    does not escape anything itself, it only builds the envelope.
    """
    prosody_open = f"<prosody rate='{rate}'>" if rate else ""
    prosody_close = "</prosody>" if rate else ""
    return (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='pt-BR'>"
        f"<voice name='{voice}'>{prosody_open}{tagged_text}{prosody_close}</voice>"
        "</speak>"
    )


def build_segment_ssml(plain_text: str, cleaner) -> str:
    """Compose the full SSML document for one segment: escape -> insert breaks -> envelope.

    This exact order matters: escaping must happen before break-tag insertion,
    never after, or the inserted <break> tags would themselves get escaped into
    literal text and read aloud.
    """
    voice = os.getenv("AZURE_SPEECH_VOICE", DEFAULT_VOICE)
    rate = os.getenv("AZURE_SPEECH_RATE")
    escaped = _xml_escape(plain_text)
    tagged = cleaner.insert_speech_breaks(escaped)
    return build_ssml(tagged, voice=voice, rate=rate)


def generate_tts(text: str, output_path: str, use_ssml: bool = False):
    speech_config = _build_speech_config()
    audio_config = speechsdk.audio.AudioOutputConfig(filename=str(Path(output_path)))
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    if use_ssml:
        speech_synthesis_result = speech_synthesizer.speak_ssml_async(text).get()
    else:
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        cancellation_details = speech_synthesis_result.cancellation_details
        raise RuntimeError(
            f"Azure speech synthesis failed: {speech_synthesis_result.reason}. {cancellation_details.reason}: {cancellation_details.error_details}"
        )

    return speech_synthesis_result