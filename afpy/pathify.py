from pathlib import Path
import os

def pathify(path:str):
        path = str_to_raw(path)
        if os.path.isdir(path) or os.path.isfile(path):
            return Path(path)
        else:
            return False

def str_to_raw(string:str):
    return r'{}'.format(string)