from typing import Tuple, Union

from base_reader import BaseReader


class DateHierarchyReader(BaseReader):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.file_pointer = open(path, "r")
        self.isFirstLine = True

    def readline(self) -> Union[str, None]:
        if self.isFirstLine:
            # tossing header away
            self.file_pointer.readline()
            self.isFirstLine = False
        line = self.file_pointer.readline()
        if not line:
            return None
        identifier, dia, mes = line.replace('"', "").split(",")
        dia = str(int(float(dia)))
        mes = str(int(float(mes)))
        if int(dia) < 10:
            dia = "0" + dia
        if int(mes) < 10:
            mes = "0" + mes
        subdirectory = f"{mes}/{dia}/{identifier}/"
        return subdirectory
