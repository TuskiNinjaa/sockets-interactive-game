import pickle


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class ClientSender:
    """
        Helper class responsible for grouping
        client requests/responses in communication with the server
        """
    def __init__(self, socket, buffer_size):
        self.socket = socket
        self.buffer_size = buffer_size

    def close(self):
        self.socket.close()

    def request(self, request_type):
        request = {"type": request_type}
        self.socket.send(pickle.dumps(request))

    def request_message(self, message):
        self.socket.send(pickle.dumps(message))

    def request_receive(self, request_type):
        self.request(request_type)
        return pickle.loads(self.socket.recv(self.buffer_size))

    def request_receive_message(self, message):
        self.socket.send(pickle.dumps(message))
        return pickle.loads(self.socket.recv(self.buffer_size))
