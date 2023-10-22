from sender import ClientSender
from user import User
from Message import Message

class Menu:
    def __init__(self, name, socket, buffer_size):
        self.name = name
        self.sender = ClientSender(socket, buffer_size)
        self.user = User()

        self.menu_string = "-------------------------"
        
    def get_user(self):
        return self.user
    
    def exit_server(self):
        self.sender.request(Message.type_exit_server)

    def invalid_request(self):
        run_menu = True
        while run_menu:
            try:
                option = int(input("[%s] Invalid request. Select an option:\n0 - Try again\n1 - Exit\nAnswer: " %(self.name)))

                if option == 0: # Try again
                    return True
                elif option == 1: # Exit menu
                    return False
                else:
                    print("[%s] Select an valid option." % self.name)
        
            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)

    def option_login_account(self):
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"      : Message.type_login,
            "nickname"  : nickname,
            "password"  : password
        }

        return self.sender.request_receive_message(request)
    
    def option_create_account(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"       : Message.type_create_account,
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
                self.sender.request(Message.type_lobby)
                return False

            run_request = self.invalid_request()

        return True
    
    def login(self):
        run_menu = True
        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - Login\n1 - Create account\n2 - Exit\nAnswer: "%(self.name)))

                if option == 0: # Simple login
                    run_menu = self.option_account(self.option_login_account)
                elif option == 1: # Account creation and login
                    run_menu = self.option_account(self.option_create_account)
                elif option == 2:
                    run_menu = False
                else: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)

            print(self.menu_string)

    def option_list(self, request_type):
        response = self.sender.request_receive(request_type)
        list_received = response.get("list")

        if request_type == Message.type_list_user_on_line:
            template = "|{:^15}|{:^10}|{:^15}|{:^5}|"
            print(self.menu_string)
            print(template.format("Nickname", "Status", "IP", "Port"))
        else:
            template = "{:15} ({:^15}:{:5}) x {:15} ({:^15}:{:5})"
            print(self.menu_string)
            print(template.format("Host Nickname", "IP", "Port", "Player Nickname", "IP", "Port"))

        for line in list_received:
            print(template.format(*line))
    
    def option_request_connection(self):
        response = self.sender.request_receive(Message.type_list_user_idle)
        list_received = response.get("list")

        # print("[%s] Request connection, choose one or more users:" % self.name)
        # template = "{:^5} - |{:^15}|{:^15}|{:^5}|"
        # print(template.format("Index", "Nickname", "IP", "Port"))

        # for key, value in enumerate(list_received):
        #     print(template.format(key, *value))

        # raw_users = input("Selected users:")
        # users_indices = raw_users.split(',')

        # selected_users = []
        # for i in users_indices:
        #     selected_users.append(list_received[int(i)])
        #     # self.__send_game_in(list_received[int(i)])

        # print("[%s] Selected users %s."%(selected_users))

        print("[%s] Response: %s" %(self.name, response))

    def option_wait_connection(self): # Implements the process of listening to a client request to start a game
        request = {
            "type": Message.type_game,
            "request": False
        }

        response = self.sender.request_receive_message(request)

        print("[%s] Response: %s" %(self.name, response))

    def lobby(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - LIST-USER-ON-LINE\n1 - LIST-USER-PLAYING\n2 - Request connection\n3 - Wait for request\n4 - Exit\nAnswer: "%(self.name)))

                if option == 0: # LIST-USER-ON-LINE
                    self.option_list(Message.type_list_user_on_line)
                elif option == 1: # LIST-USER-PLAYING
                    self.option_list(Message.type_list_user_playing)
                elif option == 2: # Request an connection with other players
                    self.option_request_connection()
                elif option == 3: # Wait for an connection request
                    self.option_wait_connection()
                elif option == 4:
                    run_menu = False
                else: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            
            print(self.menu_string)

    def __start_connection(self):
        response = self.sender.request_receive(self.sender.type_list_user_idle)
        list_received = response.get("list")
        if not list_received:
            print("[%s] No users available found, please try later\n" % self.name)
            return

        print("[%s] Request connection, choose one or more users:" % self.name)
        template = "{:^5} - |{:^15}|{:^15}|{:^5}|"
        print(template.format("Index", "Nickname", "IP", "Port"))

        for key, value in enumerate(list_received):
            print(template.format(key, *value))

        raw_users = input("Selected users:")
        users_indices = raw_users.split(',')

        selected_users = []

        for i in users_indices:
            selected_users.append(list_received[int(i)])

            # self.__send_game_in(list_received[int(i)])

        request = {
            "type" : self.sender.type_game,
        }

    def __send_game_in(self, user):
        print("")
        #todo criar coneção com outro cliente perguntando se quer se conectar
        #caso positivo avisar servidor
