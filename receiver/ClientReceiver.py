import pickle
from Game import Game
from Message import Message
from sender import ClientSender

class ClientReceiver:
    def __init__(self, name, connection, address, sender, buffer_size, user):
        self.name = name
        self.connection = connection
        self.address = address
        self.sender = sender
        self.buffer_size = buffer_size
        self.user = user
        self.menu_string = "-------------------------"

    def print_message(self, menu_name, message_name, message):
        print("[%s] %s\n%s: %s\nAddress: %s" %(self.name, menu_name, message_name, message, self.address))

    def menu(self):
        request = pickle.loads(self.connection.recv(self.buffer_size))
        response = {}
        start_game = False

        run_menu = True
        while run_menu:
            try:
                option = int(input("[%s] Do you want to play with %s? Select an option:\n0 - No\n1 - Yes\nAnswer: " %(self.name, request.get("host_nickname"))))

                if option == 0: # Disconnect
                    response.update({"type": Message.type_finish_game})
                    start_game = False
                    run_menu = False
                elif option == 1: # Connect
                    response.update({"type": Message.type_init_game})
                    start_game = True
                    run_menu = False
                else:
                    print("[%s] Select an valid option." % self.name)
        
            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)
        
        self.connection.send(pickle.dumps(response))
        return start_game

    def handle_connection(self):
        try:
            start_game = self.menu()

            if start_game:
                game = Game(self.user)
                message = game.handle_player(self.connection, self.buffer_size)

                response = self.sender.request_receive_message(message)
            
            self.connection.close()

        except (EOFError, ConnectionResetError) as e:
            print("[%s] ERROR: Connection lost."%(self.name))
            self.connection.close()
            
            request = {
                "type": Message.type_update_game.value,
                "is_loser": True
            }
            response = self.sender.request_receive_message(request)
        except KeyboardInterrupt as e:
            print("[%s] Game closed."%self.name)
            request = {
                "type": Message.type_update_game.value,
                "is_loser": True
            }
            response = self.sender.request_receive_message(request)