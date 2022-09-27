
import yaml 
from yaml import Loader, Dumper
from .pathify import *

class yml:
        def __init__(self):
            pass
        def dump(self, 
            data, 
            path : str
        ):
            '''Dumps incoming python data into a YAML file at `path`.
            
            -----
            * `data` (dict,list,tuple) : Any YAML dump friendly python data structure.
            * `path` (str) : Path to YAML output file.
            '''
            with open(path, "w") as output_file:
                yaml.dump(data, output_file, Dumper=yaml.Dumper)

        def load(self, 
            path : str
        ):
            '''Loads YAML data from a file at the provided path.
            
            -----
            * `path` (str) : Path to YAML file.
            * `return` (dict,list,tuple) : Returns a python data structure.
            '''
            path = pathify(path)
            with open(path,'r') as input_file:
                return yaml.load(input_file, Loader=yaml.Loader)