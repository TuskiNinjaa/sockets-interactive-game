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
        return "%s"%self.server_port
    
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
    
    def login_account_verification(self, request):
        # Implementation the process of verification of the login account and make return True or False if the user is online        
        nickname = request.get("nickname")
        password = request.get("password")

        response = {"type": "login"}
        if nickname == "wrong_nickname" or password == "wrong_password":
            # Condition when something went wrong on login
            response.update({"logged": False})
        else:
            response.update({"full_name": "FullNameSample"})
            response.update({"nickname": nickname})
            response.update({"logged": True})

        return response
    
    def create_account_verification(self, request):
        # Implementation of the process of profile creation and login on new account if possible
        full_name = request.get("full_name")
        nickname = request.get("nickname")
        password = request.get("password")

        response = {"type": "create_account"}
        if full_name == "wrong_full_name" or nickname == "wrong_nickname" or password == "wrong_password":
            #Condition when something went wrong on account creation
            response.update({"logged": False})
        else:
            response.update({"full_name": full_name})
            response.update({"nickname": nickname})
            response.update({"logged": True})

        return response
    
    def handle_menu_login(self, connection, address):
        request = pickle.loads(connection.recv(self.buffer_size))
        print("[%s] LOGIN\nRequest: %s\nAddress: %s" %(self.name, request, address))

        while request.get("type") != "lobby" and request.get("type") != "exit_server":
            match request.get("type"):
                case "login":
                    response = self.login_account_verification(request)

                case "create_account":
                    response = self.create_account_verification(request)

                case _:
                    response = "[%s] Unknown type of request."%self.name

            print("[%s] LOGIN\nResponse: %s\nAddress: %s"%(self.name, response, address))

            connection.send(pickle.dumps(response))
            request = pickle.loads(connection.recv(self.buffer_size))
            print("[%s] LOGIN\nRequest: %s\nAddress: %s" %(self.name, request, address))
        
        return request
    
    def handle_menu_lobby(self, connection, address):
        print("[%s] %s is connected to the Lobby."%(self.name, address))

    def handle_connection(self, connection, address):
        try:
            request = self.handle_menu_login(connection, address)
            if request.get("type") == "lobby": # Verify if the user is logged
                self.handle_menu_lobby(connection, address)
            
            connection.close()
            print("[%s] Connection to %s is closed."%(self.name, address))

        except (EOFError, ConnectionResetError) as e:
            print("[%s] ERROR %s lost connection."%(self.name, address))
            connection.close()

    def listen_to_client(self):
        try:
            self.socket.listen(1)
            while True:
                connection, address = self.socket.accept()
                thread = threading.Thread(target=self.handle_connection, args=(connection, address))
                thread.daemon = True
                thread.start()

                print("[%s] Active connections: %d" %(self.name, threading.active_count() - 2))
                
        except (KeyboardInterrupt) as e:
            self.shutdown_server()
    
    def listen_to_terminal(self):
        while True:
            teste = input()
            print(teste)

    def listen_threads(self):
        thread_terminal = threading.Thread(target=self.listen_to_terminal, args=())
        thread_terminal.daemon = True
        thread_terminal.start()

        self.listen_to_client()

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
    server.listen_threads()

if __name__ == "__main__":
    main()
    sys.exit(0)

# Implementar
#   login
#       
#   monitoramento de usuários
#