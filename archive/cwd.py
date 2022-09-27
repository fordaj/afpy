import os
from pathlib import Path


def cwd(file):
    return Path(os.path.dirname(os.path.realpath(file)))