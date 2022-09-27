import platform, os
from pathlib import Path

class Formatter:
    def __init__(self):
        pass

    def path(self, 
        path:str=None
    ) -> str:
        ''' Returns an OS-agnostic path string.
        
        -----
        * `path` (str) : A path to a directory or file.
        * `return` (str) : Properly formatted path string.
        '''
        if (path == None):
            path = os.getcwd()
        path = path.replace('"','')
        path = path.replace("'",'')
        if platform.system() == 'Windows':
            path.replace('/','\\')
        else:
            path.replace('\\','/')
        return Path(path)