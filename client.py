import socket
import pickle

class Client:
    def __init__(self, server_ip, server_port, buffer_size, encoding):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.encoding = encoding

        self.is_connected = False
        self.name = ""
        self.ip = ""
        self.port = 1500

    def connect_to_server(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        message = {
            "full_name": full_name,
            "nickname" : nickname,
            "password" : password
        }

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.server_port))

        client_socket.send(pickle.dumps(message))

        response = client_socket.recv(self.buffer_size)

        print ("Response: ", response)

        client_socket.close()

SERVER_IP = "10.0.0.103"
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    client = Client(server_ip=SERVER_IP, server_port=SERVER_PORT, buffer_size=BUFFER_SIZE, encoding=ENCODING)
    client.connect_to_server()

if __name__ == "__main__":
    main()