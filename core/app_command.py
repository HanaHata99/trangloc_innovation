from enum import Enum
from multiprocessing import Queue, Pipe
from queue import Empty
import threading
from typing import Callable

class CommandType(Enum):
    STOP_WEB_SERVER = 1
    SUMMER = 2
    AUTUMN = 3
    WINTER = 4

class AppCommand:
    def __init__(self, cmdType:CommandType, data:str=''):
        self.type:CommandType = cmdType
        self.data:str = data

    @classmethod
    def create(cls, cmdType:CommandType, data:str=''):
        cmd:AppCommand = AppCommand(cmdType, data)
        return cmd

class CommandInterface:
    def __init__(self):
        self.listening:bool = False
        self.command_queue:Queue = Queue()

    def start_interface(self):
        self.listening:bool = True
        threading.Thread(target=self.verify, daemon=True).start()
    
    def stop_interface(self):
        self.listening:bool = False

    def verify(self):
        while True == self.listening:
            try:
                cmd:AppCommand = self.command_queue.get(timeout=1)
                if None == cmd:
                    break
                self.command_callback(cmd)
                    
            except Empty:
                pass

    def command_callback(self, cmd:AppCommand):
        pass
    
    def get_command_queue(self):
        return self.command_queue