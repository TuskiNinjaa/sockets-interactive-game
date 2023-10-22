import socket
import pickle

class ClientSender:
    def __init__(self, socket, buffer_size):
        self.socket = socket
        self.buffer_size = buffer_size

        self.type_exit_server = "EXIT-SERVER"
        self.type_login = "LOGIN"
        self.type_create_account = "CREATE-ACCOUNT"
        self.type_list_user_on_line = "LIST-USER-ON-LINE"
        self.type_list_user_playing = "LIST-USER-PLAYING"
        self.type_list_user_idle = "LIST-USER-IDLE"
        self.type_lobby = "LOBBY"
        self.type_game = "GAME"

    def request(self, request_type):
        request = {"type": request_type}
        self.socket.send(pickle.dumps(request))

    def request_receive(self, request_type):
        self.request(request_type)
        return pickle.loads(self.socket.recv(self.buffer_size))
    
    def request_receive_message(self, message):
        self.socket.send(pickle.dumps(message))
        return pickle.loads(self.socket.recv(self.buffer_size))