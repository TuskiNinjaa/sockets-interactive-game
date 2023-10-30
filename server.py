import socket
import sys
import threading

from receiver.ServerReceiver import ServerReceiver


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class Server:
    def __init__(self, name, ip, port, buffer_size, encoding):
        self.name = name
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = self.start_server()
        self.encoding = encoding

    def __str__(self):
        return "%s" % self.port

    def start_server(self):
        print("[%s] Initializing server." % self.name)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        return server_socket

    def shutdown_server(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print("\n[%s] Shutting down server." % self.name)

    def listen_to_client(self):
        try:
            self.socket.listen(1)
            receiver = None
            while True:
                connection, address = self.socket.accept()
                receiver = ServerReceiver("%s" % (self.name), connection, address, self.buffer_size)

                thread = threading.Thread(target=receiver.handle_connection, args=())
                thread.daemon = True
                thread.start()

                print("[%s] Active connections: %d" % (self.name, threading.active_count() - 1))

        except (KeyboardInterrupt) as e:
            if receiver != None:
                receiver.exit_connection()
            self.shutdown_server()


SERVER_NAME = "SERVER"
SERVER_IP = "localhost"
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
