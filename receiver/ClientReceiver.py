import pickle

class ClientReceiver:
    def __init__(self, name, connection, address, buffer_size):
        self.name = name
        self.connection = connection
        self.address = address
        self.buffer_size = buffer_size

    def print_message(self, menu_name, message_name, message):
        print("[%s] %s\n%s: %s\nAddress: %s" %(self.name, menu_name, message_name, message, self.address))

    def handle_connection(self):
        try:
            request = pickle.loads(self.connection.recv(self.buffer_size))
            response = "OK"
            self.connection.send(pickle.dumps(response))

            self.print_message("Client", "Request", request)
            self.print_message("Client", "Response", response)

        except (EOFError, ConnectionResetError) as e:
            print("[%s] ERROR %s lost connection."%(self.name, self.address))
            self.connection.close()