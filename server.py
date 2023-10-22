import sys
import socket
import threading
from receiver import ServerReceiver

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
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print("\n[%s] Shutting down server."%self.name)

    def listen_to_client(self):
        try:
            self.socket.listen(1)
            while True:
                connection, address = self.socket.accept()
                receiver = ServerReceiver("%s"%(self.name), connection, address, self.buffer_size)

                thread = threading.Thread(target=receiver.handle_connection, args=())
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
        encoding=ENCODING,
    )

    server.listen_to_client()

if __name__ == "__main__":
    main()
    sys.exit(0)