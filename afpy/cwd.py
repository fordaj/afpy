import os
from pathlib import Path


class cwd:
    def __init__(self, file):
        return Path(os.path.dirname(os.path.realpath(file)))