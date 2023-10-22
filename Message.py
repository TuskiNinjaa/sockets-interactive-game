
from enum import Enum

class Message(Enum):
    type_exit_server = "EXIT-SERVER"
    type_login = "LOGIN"
    type_create_account = "CREATE-ACCOUNT"
    type_list_user_on_line = "LIST-USER-ON-LINE"
    type_list_user_playing = "LIST-USER-PLAYING"
    type_list_user_idle = "LIST-USER-IDLE"
    type_lobby = "LOBBY"
    type_game = "GAME"