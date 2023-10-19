import sys
import socket
import pickle
import threading

class Server:
    def __init__(self, name, ip, port, buffer_size, encoding):
        self.name = name
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = self.start_server()
        self.encoding = encoding
    
    def __str__(self):
        return f"{self.server_port}"
    
    def start_server(self):
        print("[START] Initializing server.")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        return server_socket
    
    def shutdown_server(self):
        print("\n[STOP] Shutting down server.\n")
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    
    def login_verification(self, message):
        full_name = message.get("full_name")
        nickname = message.get("nickname")
        password = message.get("password")
        
        print("Full_name: %s | Nickname: %s | Password: %s" %(full_name, nickname, password))

        return "[%s] %s"%(self.name, full_name.upper())
    
    def create_profile(self, message):

        return "[%s] It's time to create your profile"%(self.name)
    
    def handle_menu_login(self, message, connection, address):
        match message.get("message_type"):
            case "login":
                response = self.login_verification(message)

            case "create_profile":
                response = self.create_profile()

            case _:
                response = "[%s] Unknown type of message"

        # Send response of the login status
        connection.send(response.encode(self.encoding))

        print("Sent back to Client: %s | Address: %s" %(response, address))

    def handle_client(self, connection, address):
        message = connection.recv(self.buffer_size)
        message = pickle.loads(message)

        self.handle_menu_login(message, connection, address)
        
        connection.close()


    def listen_to_client(self):
        self.socket.listen(1)

        while True:
            connection, address = self.socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()

            print("[INFO] Active connections: %d" %(threading.active_count() - 1))


SERVER_NAME = "SERVER"
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    server = Server(name=SERVER_NAME, ip=SERVER_IP, port=SERVER_PORT, buffer_size=BUFFER_SIZE, encoding=ENCODING)
    print(SERVER_IP)

    try:
        server.listen_to_client()
    except (KeyboardInterrupt):
        server.shutdown_server()
    
    sys.exit(0)

if __name__ == "__main__":
    main()

# Implementar
#   login
#   monitoramento de usuários
#