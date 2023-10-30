import pickle

from Game import Game
from Message import Message


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class ClientReceiver:
    """
    Class to group logic relative to the client open sockets

    This is used on P2P connection with the game host
    opened on the game start.
    Handle the game prompt, since the game request, game
    actions till the end (handling victory or defeat)
    """
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

    """
    This method handles the game prompt.
    Querying the user if they want (or not) to accept the 
    game invitation.
    """
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


    """
    Inits the P2P connection with the game prompt
    
    Checks if the client accepts the game requests
    if yes, starts the game and handles the recieved data from host
    if not, only closes the connection
    """
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