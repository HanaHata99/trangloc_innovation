import requests
from core.eed import EEDComputor

def call_viettel_api(audiofile, causosanh):
    url = "https://viettelai.vn/asr/recognize"
    payload={'token': '9b9d4ccf61bc0ffae344cce31'}
    files=[
    ('file',('$AUDIO_FILE',open(audiofile,'rb'),'audio/wav'))
    ]
    headers = {
    'accept': '*/*'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)


    ketqua = response.json()
    hypothesis = ketqua['response']['result'][0]['transcript']

    EEDComputor.report(causosanh, hypothesis)