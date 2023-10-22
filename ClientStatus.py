from enum import Enum

class ClientStatus(Enum):
    OFFLINE = 'OFFLINE'
    IDLE = 'IDLE'
    PLAYING = 'PLAYING'