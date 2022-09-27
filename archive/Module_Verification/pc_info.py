# Author: Andrew Ford, Laurent Laporte
# Credit: https://stackoverflow.com/users/1513933/laurent-laporte
# Post: https://stackoverflow.com/questions/8220108/how-do-i-check-the-operating-system-in-python 

import platform, psutil

class Cores:
    def __init__(self):
        self.physical = psutil.cpu_count(logical=False)
        self.total = psutil.cpu_count(logical=True)

class Frequency:
    def __init__(self):
        self.max = psutil.cpu_freq().max
        self.min = psutil.cpu_freq().min

class Cpu:
    def __init__(self):
        self.cores = Cores()
        self.frequency = Frequency()

class Memory:
    def __init__(self):
        svmem = psutil.virtual_memory()
        self.total = svmem.total
        self.available = svmem.available
        self.used = svmem.used
        self.percent = svmem.percent

class PcInfo:
    def __init__(self):
        if platform.system() == "Linux" or platform.system() == "linux2":
            self.os = "linux"
        elif platform.system() == "Darwin":
            self.os = "macos"
        elif platform.system() == "win32":
            self.os = "windows"
        else:
            self.os = "unknown"
        self.hostname = platform.node()
        self.release = platform.release()
        self.version = platform.version()
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.cpu = Cpu()
        self.memory = Memory()
        
    def verify(self, os:str=None, hostname:str=None, release:str=None, version:str=None, machine:str=None, processor:str=None)->bool:
        if os is not None:
            if os.lower() != self.os:
                return False
        if hostname is not None:
            if hostname.lower() != self.hostname:
                return False
        if release is not None:
            if release.lower() != self.release:
                return False
        if version is not None:
            if version.lower() != self.version:
                return False
        if machine is not None:
            if machine.lower() != self.machine:
                return False
        if processor is not None:
            if processor.lower() != self.processor:
                return False
        return True



print("hey")