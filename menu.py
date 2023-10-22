from sender import ClientSender
from user import User

class Menu:
    def __init__(self, name, socket, buffer_size):
        self.name = name
        self.sender = ClientSender(socket, buffer_size)
        self.user = User()

        self.menu_string = "-------------------------"
        
    def get_user(self):
        return self.user
    
    def exit_server(self):
        self.sender.request(self.sender.type_exit_server)

    def invalid_request(self):
        run_menu = True
        while run_menu:
            try:
                option = int(input("[%s] Invalid request. Select an option:\n0 - Try again\n1 - Exit\nAnswer: " %(self.name)))
            
                match option:
                    case 0: # Try again
                        return True

                    case 1: # Exit menu
                        return False

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)
        
            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)

    def option_login_account(self):
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"      : self.sender.type_login,
            "nickname"  : nickname,
            "password"  : password
        }

        return self.sender.request_receive_message(request)
    
    def option_create_account(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"       : self.sender.type_create_account,
            "full_name"  : full_name,
            "nickname"   : nickname,
            "password"   : password
        }

        return self.sender.request_receive_message(request)
    
    def option_account(self, request_function):
        run_request = True
        while run_request:
            response = request_function()

            if response.get("logged"):
                self.user.set_info(response.get("full_name"), response.get("nickname"), True)
                self.sender.request(self.sender.type_lobby)
                return False

            run_request = self.invalid_request()

        return True
    
    def login(self):
        run_menu = True
        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - Login\n1 - Create account\n2 - Exit\nAnswer: "%(self.name)))

                match option:
                    case 0: # Simple login
                        run_menu = self.option_account(self.option_login_account)
                        
                    case 1: # Account creation and login
                        run_menu = self.option_account(self.option_create_account)

                    case 2: # Exit
                        run_menu = False

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)
        
            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)

            print(self.menu_string)

    def option_list(self, request_type):
        response = self.sender.request_receive(request_type)
        list_received = response.get("list")

        if request_type == self.sender.type_list_user_on_line:
            template = "|{:^15}|{:^10}|{:^15}|{:^5}|"
            print(template.format("Nickname", "Status", "IP", "Port"))
        else:
            template = "{:15} ({:>15}:{:5}) x {:15} ({:>15}:{:5})"
            print("Host Nickname (IP:Port) x Player Nickname (IP:Port)")

        for line in list_received:
            print(template.format(*line))

    def option_request_connection(self): # Implements the process of requesting the star of a game
        request = {
            "type": self.sender.type_game,
            "status": True
        }

        response = self.sender.request_receive_message(request)

        print("[%s] Response: %s" %(self.name, response))

    def option_wait_connection(self): # Implements the process of listening to a client request to start a game
        request = {
            "type": self.sender.type_game,
            "status": False
        }

        response = self.sender.request_receive_message(request)

        print("[%s] Response: %s" %(self.name, response))

    def lobby(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - LIST-USER-ON-LINE\n1 - LIST-USER-PLAYING\n2 - Request connection\n3 - Wait for request\n4 - Exit\nAnswer: "%(self.name)))

                match option:
                    case 0: # LIST-USER-ON-LINE
                        self.option_list(self.sender.type_list_user_on_line)
                        
                    case 1: # LIST-USER-PLAYING
                        self.option_list(self.sender.type_list_user_playing)
                    
                    case 2: # Request connection to player
                        self.option_request_connection()

                    case 3: # Wait for an connection request
                        self.option_wait_connection()

                    case 4: # Exit menu
                        run_menu = False

                    case _: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)