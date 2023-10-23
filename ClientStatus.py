from enum import Enum

class ClientStatus(Enum):
    OFFLINE = 'OFFLINE'
    IDLE = 'IDLE'
    READY_TO_CONNECT = 'READY_TO_CONNECT'
    PLAYING = 'PLAYING'