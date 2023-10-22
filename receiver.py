import socket
import pickle

class ServerReceiver:
    def __init__(self, name, connection, address, buffer_size):
        self.name = name
        self.connection = connection
        self.address = address
        self.buffer_size = buffer_size

        self.type_exit_server = "EXIT-SERVER"
        self.type_login = "LOGIN"
        self.type_create_account = "CREATE-ACCOUNT"
        self.type_list_user_on_line = "LIST-USER-ON-LINE"
        self.type_list_user_playing = "LIST-USER-PLAYING"
        self.type_lobby = "LOBBY"
        self.type_game = "GAME"
    
    def login_account_verification(self, request):
        # Implementation the process of verification of the login account and make return True or False if the user is online        
        nickname = request.get("nickname")
        password = request.get("password")

        response = {"type": self.type_login}
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

        response = {"type": self.type_create_account}
        if full_name == "wrong_full_name" or nickname == "wrong_nickname" or password == "wrong_password":
            #Condition when something went wrong on account creation
            response.update({"logged": False})
        else:
            response.update({"full_name": full_name})
            response.update({"nickname": nickname})
            response.update({"logged": True})

        return response
    
    def handle_menu_login(self):
        print("[%s] %s is connected to the Login Menu."%(self.name, self.address))
        request = pickle.loads(self.connection.recv(self.buffer_size))
        print("[%s] LOGIN\nRequest: %s\nAddress: %s" %(self.name, request, self.address))

        while request.get("type") != self.type_lobby and request.get("type") != self.type_exit_server:
            match request.get("type"):
                case self.type_login:
                    response = self.login_account_verification(request)

                case self.type_create_account:
                    response = self.create_account_verification(request)

                case _:
                    response = "[%s] Unknown type of request."%self.name

            print("[%s] LOGIN\nResponse: %s\nAddress: %s"%(self.name, response, self.address))

            self.connection.send(pickle.dumps(response))
            request = pickle.loads(self.connection.recv(self.buffer_size))
            print("[%s] LOGIN\nRequest: %s\nAddress: %s" %(self.name, request, self.address))
        
        return request
    
    def list_user_on_line(self):
        # Implement a way to get user informations

        user_on_line = [
            ["Fulano_1", "Status_1", "IP_1", "PORT_1"],
            ["Fulano_2", "Status_2", "IP_2", "PORT_2"],
            ["Fulano_3", "Status_3", "IP_3", "PORT_3"],
            ["Fulano_4", "Status_4", "IP_4", "PORT_4"]
        ]

        response = {
            "type": self.type_list_user_on_line,
            "list": user_on_line
        }

        return response
    
    def list_user_playing(self):
        # Implement a way to get user informations
        
        user_playing = [
            ["Fulano_1", "IP_1", "PORT_1", "Fulano_2", "IP_2", "PORT_2"],
            ["Fulano_1", "IP_1", "PORT_1", "Fulano_3", "IP_3", "PORT_3"]
        ] 

        response = {
            "type": self.type_list_user_playing,
            "list": user_playing
        }

        return response

    def handle_game(self, request):
        # Update the state of the player
        print("[%s] Handling exit game state. Request: %s"%(self.name, request))
        
        response = {
            "type": self.type_game,
            "status": request.get("status")
        }
        
        return response

    def handle_menu_lobby(self):
        print("[%s] %s is connected to the Lobby Menu."%(self.name, self.address))

        request = pickle.loads(self.connection.recv(self.buffer_size))
        print("[%s] LOBBY\nRequest: %s\nAddress: %s" %(self.name, request, self.address))

        while request.get("type") != self.type_exit_server:
            match request.get("type"):
                case self.type_list_user_on_line:
                    response = self.list_user_on_line()

                case self.type_list_user_playing:
                    response = self.list_user_playing()

                case self.type_game:
                    response = self.handle_game(request)

                case _:
                    response = "[%s] Unknown type of request."%self.name

            print("[%s] LOBBY\nResponse: %s\nAddress: %s"%(self.name, response, self.address))

            self.connection.send(pickle.dumps(response))
            request = pickle.loads(self.connection.recv(self.buffer_size))
            print("[%s] LOBBY\nRequest: %s\nAddress: %s" %(self.name, request, self.address))
        
        return request

    def handle_connection(self):
        try:
            request = self.handle_menu_login()
            
            if request.get("type") == self.type_lobby: # Verify if the user is logged
                self.handle_menu_lobby()
            
            self.connection.close()
            print("[%s] Connection to %s is closed."%(self.name, self.address))

        except (EOFError, ConnectionResetError) as e:
            print("[%s] ERROR %s lost connection."%(self.name, self.address))
            self.connection.close()
