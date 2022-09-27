from pathlib import Path
from typing import List


class Mermaid:

    def __init__(self, input_paths:List[Path], output_path:Path)->bool:
        """Compiles contents of mermaid files companion to modules.

        Args:
            input_paths (List[Path]): Folders to search for .mmd files in
            output_path (Path): Destination for compiled output .mmd file.

        Returns:
            bool: Returns `True` for success, `False` for errors
        """

        return None

    
    def hi(self):
        print("hi")