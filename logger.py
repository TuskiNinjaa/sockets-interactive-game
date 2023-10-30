from enum import Enum
from datetime import datetime


class Logs(Enum):
    CLIENT_REGISTERED = ('CLIENT_REGISTERED', " {0}  - Usuário {1} realizou cadastro \n")
    CLIENT_CONNECTED = ('CLIENT_CONNECTED', " {0}  - Usuário {1} conectou-se \n")
    CLIENT_GAME_LOST = ('CLIENT_GAME_LOST', " {0}  - Usuário {1} perdeu! \n")
    CLIENT_GAME_WON = ('CLIENT_GAME_WON', " {0}  - Usuário {1} ganhou a partida! \n")
    CLIENT_INACTIVE = ('CLIENT_INACTIVE', " {0}  - Usuário {1} tornou-se  (online, sem jogar) \n")
    CLIENT_ACTIVE = ('CLIENT_ACTIVE', " {0}  - Usuário {1} tornou-se ATIVO (online e jogando) \n")
    GAME_STARTED = ('GAME_STARTED', " {0}  - Usuários {1} começaram um jogo \n")
    CLIENT_DISCONNECTED = ('CLIENT_DISCONNECTED', " {1}  - Usuário {0} desconectou-se da rede \n")


def log(log_type: Logs, param):
    log_text = log_type.value[1].format(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), param)
    print(log_type.value[0], log_text)
    __dump_log(log_text)


def __dump_log(log_text):
    f = open("game.log", "a")
    f.write(log_text)
    f.close()
