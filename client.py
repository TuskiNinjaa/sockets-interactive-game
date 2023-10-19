import socket
import pickle

class Client:
    def __init__(self, server_ip, server_port, buffer_size, encoding):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.encoding = encoding

        self.name = "CLIENT"
        self.socket = self.connect_to_server()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 1500

        self.user_full_name = ""
        self.user_nickname = ""
        self.user_is_logged = False

    def connect_to_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.server_port))

        return client_socket
    
    def login(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        message = {
            "message_type"  : "login",
            "full_name"     : full_name,
            "nickname"      : nickname,
            "password"      : password
        }

        self.socket.send(pickle.dumps(message))
        
        response = self.socket.recv(self.buffer_size)
        print ("[%s] Response: %s" %(self.name, response))

    def create_profile(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        message = {
            "message_type"  : "create_profile",
            "full_name"     : full_name,
            "nickname"      : nickname,
            "password"      : password
        }

        self.socket.send(pickle.dumps(message))

        response = self.socket.recv(self.buffer_size)
        print ("[%s] Response: %s" %(self.name, response))

        return False
    
    def menu_login(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Hello, select an option:\n0 - Login\n1 - Create profile\n2 - Exit\nAnswer: "%(self.name)))

                match option:
                    case 0: # Login
                        run_menu = self.login()
                        
                    case 1: # Profile creation
                        run_menu = self.create_profile()

                    case 2: # Exit menu
                        print("[%s] Good bye."%self.name)
                        run_menu = False

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)

    def menu_lobby(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - LIST-USER-ON-LINE\n1 - LIST-USER-PLAYING\n2 - Exit\nAnswer: "%(self.name)))

                match option:
                    case 0: # LIST-USER-ON-LINE
                        print("[%s] LIST-USER-ON-LINE implementation"%self.name)
                        run_menu = False
                        
                    case 1: # LIST-USER-PLAYING
                        print("[%s] LIST-USER-PLAYING implementation"%self.name)
                        run_menu = self.create_profile()

                    case 2: # Exit menu
                        print("[%s] Good bye."%self.name)
                        run_menu = False

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)

    def handle_connection(self):
        self.menu_login()

        if self.user_is_logged == True:
            self.menu_lobby()

        self.socket.close()

SERVER_IP = "127.0.1.1"
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    client = Client(server_ip=SERVER_IP, server_port=SERVER_PORT, buffer_size=BUFFER_SIZE, encoding=ENCODING)
    client.handle_connection()

if __name__ == "__main__":
    main()