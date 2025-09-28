from multiprocessing import Process, Queue
from time import sleep
from core.app_config import AppConfig
from core.extractor.main_v2 import feature_worker
from models.analysis_process import analysis_worker
from models.transcribe_process import transcribe_worker
from models.vad import VadUsingRMS
from ui.server import UIServer


if __name__ == '__main__':
    appConfig:AppConfig = AppConfig()
    appConfig.load()

    audio_web_queue:Queue = Queue()
    audio_whisper_queue:Queue = Queue()
    data_queue:Queue = Queue()
    stop_queue:Queue = Queue()
    sentiment_string_queue:Queue = Queue()
    sentiment_queue:Queue = Queue()
    extractor_string_queue:Queue = Queue()
    feature_queue:Queue = Queue()
    pause_queue:Queue = Queue()
    reference_queue:Queue = Queue()

    web_server:UIServer = UIServer.create_server(audio_web_queue, data_queue, stop_queue, pause_queue, feature_queue, sentiment_queue, reference_queue)

    transcribe_process = Process(target=transcribe_worker, args=(audio_whisper_queue, sentiment_string_queue, extractor_string_queue, reference_queue), daemon=True)
    transcribe_process.start()

    analysis_process = Process(target=analysis_worker, args=(sentiment_string_queue, sentiment_queue), daemon=True)
    analysis_process.start()

    feature_process = Process(target=feature_worker, args=(extractor_string_queue, feature_queue), daemon=True)
    feature_process.start()

    vad_process:Process = VadUsingRMS.vad_worker(audio_web_queue, audio_whisper_queue, stop_queue, pause_queue)
    vad_process.start()

    web_server.run()
    vad_process.join()
    transcribe_process.join()
    analysis_process.join()