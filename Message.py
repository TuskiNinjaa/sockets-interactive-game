from enum import Enum


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class Message(Enum):
    """
        Enum Class to list possible interactions
        client/server and client/client
        """
    type_exit_server = "EXIT-SERVER"
    type_login = "LOGIN"
    type_create_account = "CREATE-ACCOUNT"
    type_list_user_on_line = "LIST-USER-ON-LINE"
    type_list_user_playing = "LIST-USER-PLAYING"
    type_list_user_ready_to_play = "LIST-USER-READY-TO-PLAY"
    type_setup_client_ready = "SETUP-USER-READY"
    type_lobby = "LOBBY"
    type_init_game = "INIT_GAME"
    type_update_game = "UPDATE_GAME"
    type_finish_game = "FINISH_GAME"
