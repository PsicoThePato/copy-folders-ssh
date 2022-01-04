from typing import Union

class BaseReader():
    """
    Encapsulates methods to get path to folders to be copied based on a file filter.
    """
    def __init__(self, path: str) -> None:
        self.path_to_file = path

    def readline(self) -> Union[str, None]:
        """
        Returns path to folder to be copied based on data of self.path_to_file.
        Must return None or other falshy value when file has ended
        """
