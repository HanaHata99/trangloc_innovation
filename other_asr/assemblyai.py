import assemblyai as aai
from core.eed import EEDComputor


aai.settings.api_key = "41b6cd84c339c60499ec9da"
config = aai.TranscriptionConfig(language_code = 'vi', speech_model=aai.SpeechModel.best)

def call_assemblyai_api(audiofile, causosanh):
    transcript = aai.Transcriber(config=config).transcribe(audiofile)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    hypothesis = transcript.text
    EEDComputor.report(causosanh, hypothesis)