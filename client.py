import sys
import socket
from menu import Menu
from user import User

class Client:
    def __init__(self, server_ip, server_port, buffer_size, encoding, name, ip, port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.encoding = encoding

        self.name = name
        self.ip = ip
        self.port = port

        self.server_socket = self.connect_to_server()
        self.client_socket = self.start_host()
        self.menu = Menu(name, self.server_socket, self.client_socket, buffer_size, ip, port)
        self.user = User()

    def connect_to_server(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((self.server_ip, self.server_port))

            return server_socket
        
        except ConnectionRefusedError as e:
            print("[%s] ERROR: Unable to connect to server."%self.name)
    
    def disconnect_to_server(self):
        self.menu.exit_server()
        self.server_socket.close()
        print("\n[%s] Disconnecting to server."%self.name)

    def start_host(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.bind((self.ip, self.port))
        print("[%s] Initializing host at %s."%(self.name, (self.ip, self.port)))
        return client_socket
    
    def shutdown_host(self):
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
        print("\n[%s] Shutting down host."%self.name)

    def handle_connection(self):
        try:
            if self.server_socket == None:
                return
            
            self.menu.login()
            self.user = self.menu.get_user()

            if self.user.logged == True:
                self.menu.lobby()

            self.disconnect_to_server()

        except (EOFError, BrokenPipeError) as e:
            print("[%s] ERROR: Connection to the server was lost. Try again later."%self.name)
            self.server_socket.close()

        except KeyboardInterrupt as e:
            self.disconnect_to_server()

SERVER_IP = "localhost"
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

CLIENT_NAME = "CLIENT"
CLIENT_IP = "localhost"
CLIENT_PORT = 1501

def main():
    client = Client(
        server_ip=SERVER_IP,
        server_port=SERVER_PORT,
        buffer_size=BUFFER_SIZE,
        encoding=ENCODING,
        name=CLIENT_NAME,
        ip=CLIENT_IP,
        port=CLIENT_PORT
    )

    client.handle_connection()


if __name__ == "__main__":
    main()
    sys.exit(0)