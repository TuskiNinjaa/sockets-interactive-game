import sys
import socket
import pickle

class Client:
    def __init__(self, server_ip, server_port, buffer_size, encoding, name, ip, port, menu_string):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.encoding = encoding

        self.name = name
        self.socket = self.connect_to_server()
        self.ip = ip
        self.port = port
        self.menu_string = menu_string

        self.user_full_name = ""
        self.user_nickname = ""
        self.user_logged = False

    def set_user_full_name(self, user_full_name):
        self.user_full_name = user_full_name

    def set_user_nickname(self, user_nickname):
        self.user_nickname = user_nickname

    def set_user_logged(self, user_logged):
        self.user_logged = user_logged

    def set_user_info(self, user_full_name, user_nickname, user_logged):
        self.set_user_full_name(user_full_name)
        self.set_user_nickname(user_nickname)
        self.set_user_logged(user_logged)

    def connect_to_server(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_ip, self.server_port))

            return client_socket
        
        except ConnectionRefusedError as e:
            print("[%s] ERROR: Unable to connect to server."%self.name)
    
    def disconnect_to_server(self):
        request = {"type": "exit_server"}
        self.socket.send(pickle.dumps(request))
        self.socket.close()

    def request_lobby(self):
        request = {"type": "lobby"}
        self.socket.send(pickle.dumps(request))

    def request_login_account(self):
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"      : "login",
            "nickname"  : nickname,
            "password"  : password
        }

        self.socket.send(pickle.dumps(request))
        return pickle.loads(self.socket.recv(self.buffer_size))
    
    def request_create_account(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"       : "create_account",
            "full_name"  : full_name,
            "nickname"   : nickname,
            "password"   : password
        }

        self.socket.send(pickle.dumps(request))
        return pickle.loads(self.socket.recv(self.buffer_size))
    
    def menu_invalid_request(self):
        run_menu = True
        while run_menu:
            try:
                option = int(input("[%s] Invalid request. Select an option:\n0 - Try again\n1 - Exit\nAnswer: " %(self.name)))
            
                match option:
                    case 0: # Try again
                        return True

                    case 1: # Exit menu
                        return False

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)
        
            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)
            
    def request_account(self, request_function):
        run_request = True
        while run_request:
            response = request_function()

            if response.get("logged"):
                self.set_user_info(response.get("full_name"), response.get("nickname"), True)
                self.request_lobby()
                return False

            run_request = self.menu_invalid_request()

        return True
    
    def menu_login(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - Login\n1 - Create account\n2 - Exit\nAnswer: "%(self.name)))

                match option:
                    case 0: # Simple login
                        run_menu = self.request_account(self.request_login_account)
                        
                    case 1: # Account creation and login
                        run_menu = self.request_account(self.request_create_account)

                    case 2: # Exit 
                        self.disconnect_to_server()
                        run_menu = False
                        print("[%s] Good bye."%self.name)

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)
        
            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)

            print(self.menu_string)

    def menu_lobby(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - LIST-USER-ON-LINE\n1 - LIST-USER-PLAYING\n2 - Exit\nAnswer: "%(self.name)))

                match option:
                    case 0: # LIST-USER-ON-LINE
                        print("[%s] LIST-USER-ON-LINE implementation"%self.name)
                        run_menu = True
                        
                    case 1: # LIST-USER-PLAYING
                        print("[%s] LIST-USER-PLAYING implementation"%self.name)
                        run_menu = True

                    case 2: # Exit menu
                        run_menu = False
                        print("[%s] Good bye."%self.name)

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)

    def handle_connection(self):
        try:
            if self.socket == None:
                return 0

            self.menu_login()

            if self.user_logged == True:
                self.menu_lobby()

        except EOFError as e:
            print("[%s] ERROR: Connection to the server was lost. Try again later."%self.name)
            self.socket.close()

        except KeyboardInterrupt as e:
            self.disconnect_to_server()


SERVER_IP = "10.0.0.102"
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

CLIENT_NAME = "CLIENT"
CLIENT_IP = "10.0.0.102"
CLIENT_PORT = 1500

MENU_STRING = "--------------------"

def main():
    client = Client(
        server_ip=SERVER_IP,
        server_port=SERVER_PORT,
        buffer_size=BUFFER_SIZE,
        encoding=ENCODING,
        name=CLIENT_NAME,
        ip=CLIENT_IP,
        port=CLIENT_PORT,
        menu_string=MENU_STRING
    )

    client.handle_connection()


if __name__ == "__main__":
    main()
    sys.exit(0)