from enum import Enum


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class ClientStatus(Enum):
    """
    Enum class reponsible for listing the possible client status
    """
    OFFLINE = 'OFFLINE'
    IDLE = 'IDLE'
    PLAYING = 'PLAYING'
