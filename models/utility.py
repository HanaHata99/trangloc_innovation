
from multiprocessing import Value


class ShareCounter:
    def __init__(self, is_parent:bool, max_val:int=0, share_value=None):
        self.is_parent = is_parent
        self.max_val = max_val
        if True == is_parent:
            self.share_value = Value('i', 0)
        else:
            self.share_value = share_value

    def ready(self) -> bool:
        result:bool = False
        if True == self.is_parent:
            with self.share_value.get_lock():
                result = self.share_value.value >= self.max_val
        
        return result

    def increase(self):
        if False == self.is_parent:
            with self.share_value.get_lock():
                self.share_value.value += 1