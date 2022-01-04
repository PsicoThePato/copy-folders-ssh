from dotenv import load_dotenv
from os import getenv

load_dotenv()

class ServerParams:
    def __init__(self) -> None:
        self.usr = getenv('USR')
        self.passwd = getenv('PASSWD')
        self.host = getenv('HOST')

CONNECTION_PARAMS = ServerParams()
ROOTPATH = getenv('ROOTPATH')
FILENAMESPATH = getenv('FILENAMESPATH')