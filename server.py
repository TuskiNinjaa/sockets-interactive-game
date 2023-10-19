import sys
import socket
import pickle

class Server:
    def __init__(self, server_ip, server_port, buffer_size, encoding):
        self.ip = server_ip
        self.port = server_port
        self.buffer_size = buffer_size
        self.socket = self.start_server()
        self.encoding = encoding

    
    def __str__(self):
        return f"{self.server_port}"
    
    def start_server(self):
        print("Initializing server.")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(1)

        return server_socket
    
    def shutdown_server(self):
        print("\nShutting down server.\n")
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def start_listening_login(self):  
        while True:
            connection_socket, address = self.socket.accept()
            
            message = connection_socket.recv(self.buffer_size)
            message = pickle.loads(message)

            # Implementation of the login verification
            output = self.login_verification(message)
            
            # Send response of the login status
            connection_socket.send(output.encode(self.encoding))

            print("Sent back to Client: %s" %(output))
            
            connection_socket.close()
    
    def login_verification(self, message): # Raissa
        full_name = message.get("full_name")
        nickname = message.get("nickname")
        password = message.get("password")
        
        print("Full_name: %s | Nickname: %s | Password: %s" %(full_name, nickname, password))

        return full_name.upper()


SERVER_IP = "10.0.0.103"
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    server = Server(server_ip=SERVER_IP, server_port=SERVER_PORT, buffer_size=BUFFER_SIZE, encoding=ENCODING)
    
    try:
        server.start_listening_login()
    except (KeyboardInterrupt):
        server.shutdown_server()
    
    sys.exit(0)

if __name__ == "__main__":
    main()


# IMPLEMENTAR
#   Login
#
#
#