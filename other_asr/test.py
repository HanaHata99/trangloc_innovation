import json
import os

from other_asr.fpt import call_fpt_api
from other_asr.viettel import call_viettel_api
from other_asr.assemblyai import call_assemblyai_api

base_path = os.path.dirname(os.path.abspath(__file__))


def load_data():
    test_dir = os.path.join(base_path, "data_test")
    config_file = os.path.join(test_dir, "data.json")
    data_json:dict = {}
    with open(config_file, 'r', encoding='utf-8') as file:
            data_json = json.load(file)
            print(data_json)
    
    datas = data_json['data_tests']

    print("=============== AssemblyAI ===============")
    for data in datas:
        audio_file = os.path.join(test_dir, data['audiofile'])
        call_assemblyai_api(audio_file, data['text'])
        print("------------------------------------------")

    print("================ Viettel ================")
    for data in datas:
        audio_file = os.path.join(test_dir, data['audiofile'])
        call_viettel_api(audio_file, data['text'])
        print("------------------------------------------")


    print("=================== FPT ==================")
    for data in datas:
        audio_file = os.path.join(test_dir, data['audiofile'])
        call_fpt_api(audio_file, data['text'])
        print("------------------------------------------")