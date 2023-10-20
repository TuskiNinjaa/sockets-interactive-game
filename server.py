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
        print("[%s] Initializing server."%self.name)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        return server_socket
    
    def shutdown_server(self):
        print("[%s] Shutting down server."%self.name)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def login_verification(self, message):
        # Implementation the process of verification of the login account and make return True or False if the user is online        
        nickname = message.get("nickname")
        password = message.get("password")

        response = {
            "type": "login"
        }
        if nickname == "wrong_nickname" or password == "wrong_password":
            response.update({"logged": False})
        else:
            response.update({"logged": True})

        return response
    
    def create_account_verification(self, message):
        # Implementation of the process of profile creation and login on new account if possible
        full_name = message.get("full_name")
        nickname = message.get("nickname")
        password = message.get("password")

        response = {
            "type": "create_account"
        }
        if full_name == "wrong_full_name" or nickname == "wrong_nickname" or password == "wrong_password":
            response.update({"logged": False})
        else:
            response.update({"logged": True})

        return response
    
    def handle_menu_login(self, connection, address):
        message = pickle.loads(connection.recv(self.buffer_size))
        print("[%s] LOGIN\nMessage: %s\nAddress: %s" %(self.name, message, address))

        while message.get("type") != "exit_menu_login" and message.get("type") != "exit_server":
            match message.get("type"):
                case "login":
                    response = self.login_verification(message)

                case "create_account":
                    response = self.create_account_verification(message)

                case _:
                    response = "[%s] Unknown type of message."%self.name

            print("[%s] LOGIN\nResponse: %s\nAddress: %s"%(self.name, response, address))

            connection.send(pickle.dumps(response))
            message = pickle.loads(connection.recv(self.buffer_size))
            print("[%s] LOGIN\nMessage: %s\nAddress: %s" %(self.name, message, address))
        
        return message


    def handle_client(self, connection, address):
        try:
            message = self.handle_menu_login(connection, address)
            print("[%s] Connection to %s is closed."%(self.name, address))
            connection.close()

        except (EOFError, ConnectionResetError) as e:
            print("[%s] ERROR %s lost connection."%(self.name, address))
            connection.close()

    def listen_to_client(self):
        self.socket.listen(1)

        try:
            while True:
                connection, address = self.socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(connection, address))
                thread.daemon = True
                thread.start()

                print("[%s] Active connections: %d" %(self.name, threading.active_count() - 1))
        except (KeyboardInterrupt) as e:
            self.shutdown_server()

SERVER_NAME = "SERVER"
SERVER_IP = "10.0.0.102"
SERVER_PORT = 2001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    server = Server(
        name=SERVER_NAME,
        ip=SERVER_IP,
        port=SERVER_PORT,
        buffer_size=BUFFER_SIZE,
        encoding=ENCODING
    )

    server.listen_to_client()

if __name__ == "__main__":
    main()
    sys.exit(0)

# Implementar
#   login
#       
#   monitoramento de usuários
#