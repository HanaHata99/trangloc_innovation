import requests
from core.eed import EEDComputor

def call_fpt_api(audiofile, causosanh):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(audiofile, 'rb').read()
    headers = {
        'api-key': 'BMcABFqXbhs9M7kRiPNer4G'
    }

    response = requests.post(url=url, data=payload, headers=headers)

    ketqua = response.json()
    hypothesis = ketqua['hypotheses'][0]['utterance']

    EEDComputor.report(causosanh, hypothesis)