from enum import Enum


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class GameStatus(Enum):
    """
        Enum class reponsible for listing the possible game status
        """
    RUNNING = 'RUNNING'
    CANCELED = 'CANCELED'
    FINISHED = 'FINISHED'
