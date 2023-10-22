from enum import Enum
from datetime import datetime


class Logs(Enum):
    CLIENT_CONNECTED = ('CLIENT_CONNECTED', " %s  - Usuário {0} conectou-se \n")
    CLIENT_NOT_RESPONDING = ('CLIENT_NOT_RESPONDING', " %s  - Usuário {0}  não responde (morreu) \n")
    CLIENT_INACTIVE = ('CLIENT_INACTIVE', " %s  - Usuário {0} tornou-se INATIVO \n")
    CLIENT_ACTIVE = ('CLIENT_ACTIVE', " %s  - Usuário {0} tornou-se ATIVO \n")
    GAME_STARTED = ('CLIENT_ACTIVE', " %s  - Usuários {0} começaram um jogo \n")
    CLIENT_DISCONNECTED = ('CLIENT_DISCONNECTED', " %s  - Usuário {0} desconectou-se da rede \n")


def log(log_type: Logs, param):
    log_text = log_type.value[1].format(datetime.now().strftime("%H:%M:%S"), param)
    print(log_type.value[0], log_text)
    __dump_log(log_text)


def __dump_log(log_text):
    f = open("game.log", "a")
    f.write(log_text)
    f.close()
