import os, json, torch

class AppConfig:
    BASE_PATH:str = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE:str = 'config.json'
    instance = None


    sample_rate       = 16000       # Hz
    blocksize         = 1024        # frames per callback
    loading_duration   = 5.0        # seconds for initial background fill
    buffer_size       = int(sample_rate * loading_duration)
    frame_size        = 1024        # window for envelope RMS
    k                 = 4.0         # dynamic threshold factor
    # MIN_RMS           = 0.02        # fixed minimum RMS to consider valid speech
    silence_window    = 1.0         # seconds window to evaluate RMS for continuation
    min_record_time   = 0.5         # minimum recording duration (seconds)
    device = (
        "cuda" if torch.cuda.is_available() else
        "mps" if torch.backends.mps.is_available() else
        "cpu"
    )
    external_config:dict = {}

    def __init__(self):
        self.dictionary = {}
        AppConfig.instance = self
    
    @classmethod
    def get_instance(cls):
        if None == AppConfig.instance:
            config:AppConfig = AppConfig()
            config.load()
        return AppConfig.instance

    @classmethod
    def width(cls):
        config:AppConfig = AppConfig.get_instance()
        result = config.dictionary['width']
        return result

    @classmethod
    def height(cls):
        config:AppConfig = AppConfig.get_instance()
        result = config.dictionary['height']
        return result

    @classmethod
    def is_debug(cls):
        config:AppConfig = AppConfig.get_instance()
        result:bool = config.dictionary['debug']
        return result

    @classmethod
    def using_webview(cls):
        config:AppConfig = AppConfig.get_instance()
        result:bool = config.dictionary['webview']
        return result

    @classmethod
    def min_rms(cls):
        config:AppConfig = AppConfig.get_instance()
        result:float = config.dictionary['min_rms']
        return result

    @classmethod
    def set_min_rms(cls, min_rms:float):
        config:AppConfig = AppConfig.get_instance()
        config.dictionary['min_rms'] = min_rms

    @classmethod
    def figure_limit(cls):
        config:AppConfig = AppConfig.get_instance()
        result:bool = config.dictionary['figure_limit']
        return result

    def load(self):
        try:
            config_path:str = os.path.join(AppConfig.BASE_PATH, '../', AppConfig.CONFIG_FILE)
            with open(config_path, 'r') as file:
                self.dictionary = json.load(file)
            print(f'[AppConfig.load] Đã load config thành công: {self.dictionary}')
        except Exception as ex:
            print(f'[AppConfig.load] {ex}')

    def save(self):
        try:
            json_object = json.dumps(self.dictionary, indent=4)
            config_path:str = os.path.join(AppConfig.BASE_PATH, '../', AppConfig.CONFIG_FILE)
            with open(config_path, 'w') as file:
                file.write(json_object)
            print('[AppConfig.save] Đã lưu config thành công')
        except Exception as ex:
            print(f'[Config.save] {ex}')