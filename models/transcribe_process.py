
from multiprocessing import Queue
from queue import Empty
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from core.app_config import AppConfig
from core.eed import EEDComputor
from models.silero_model import SileroVAD

def transcribe_worker(audio_queue:Queue, sentiment_string_queue:Queue, extractor_string_queue:Queue, reference_queue:Queue):
    model_name = 'vinai/PhoWhisper-small'
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name).to(AppConfig.device).eval()
    model.generation_config.forced_decoder_ids = None
    vad:SileroVAD = SileroVAD()
    print("Đã load xong model Whisper")
    current_reference:str = ''

    while True:
        try:
            reference:str = reference_queue.get(block=False)
            if None != reference:
                current_reference = reference.rstrip("!?.").lower()

        except Empty:
            pass

        try:
            item = audio_queue.get(timeout=1)
            if item is None:
                break
        except Empty:
            continue

        request_id, data = item

        result = vad.get_speechs(data)
        
        if len(result) > 0:
            # Transcribe audio
            inputs = processor(data, sampling_rate=AppConfig.sample_rate, return_tensors="pt", language='vi')
            inputs = {k: v.to(AppConfig.device) for k, v in inputs.items()}
            with torch.inference_mode():
                predicted_ids = model.generate(inputs['input_features'], language='vi')
            transcription:str= processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            print(f"[transcribe_worker] ({request_id}) → {transcription}")
            # Send to analysis process
            sentiment_string_queue.put((request_id, transcription))
            extractor_string_queue.put((request_id, transcription))
            if '' != current_reference:
                hypothesis = transcription.rstrip("!?.").lower()
                EEDComputor.report(current_reference, hypothesis)
        else:
            print(f'Không có giọng nói để chuyển sang text')
    sentiment_string_queue.put(None)
    extractor_string_queue.put(None)
    print('Transcribe process đã dừng')