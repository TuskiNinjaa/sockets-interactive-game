import socket
import threading
from sender import ClientSender
from receiver.ClientReceiver import ClientReceiver
from user import User
from Message import Message
from Game import Game

class Menu:
    def __init__(self, name, server_socket, client_socket, buffer_size):
        self.name = name
        self.sender = ClientSender(server_socket, buffer_size)
        self.buffer_size = buffer_size
        self.client_socket = client_socket
        self.user = User()

        self.menu_string = "-------------------------"
        
    def get_user(self):
        return self.user
    
    def exit_server(self):
        self.sender.request(Message.type_exit_server.value)
        self.user.set_logged(False)

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
            "type"      : Message.type_login.value,
            "nickname"  : nickname,
            "password"  : password,
            "ip"        : self.client_socket.getsockname()[0],
            "port"      : self.client_socket.getsockname()[1]
        }

        return self.sender.request_receive_message(request)
    
    def option_create_account(self):
        full_name = input("Full name: ")
        nickname = input("Nickname: ")
        password = input("Password: ")

        request = {
            "type"      : Message.type_create_account.value,
            "full_name" : full_name,
            "nickname"  : nickname,
            "password"  : password,
            "ip"        : self.client_socket.getsockname()[0],
            "port"      : self.client_socket.getsockname()[1]
        }

        return self.sender.request_receive_message(request)
    
    def option_account(self, request_function):
        run_request = True
        while run_request:
            response = request_function()

            if response.get("logged"):
                self.user.set_info(response.get("full_name"), response.get("nickname"), True)
                self.sender.request(Message.type_lobby.value)
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

        if request_type == Message.type_list_user_on_line.value:
            template = "|{:^15}|{:^10}|{:^15}|{:^5}|"
            print(self.menu_string)
            print(template.format("Nickname", "Status", "IP", "Port"))
        else:
            template = "{:15} ({:^15}:{:5})"
            print(self.menu_string)
            print(template.format("Nickname", "IP", "Port"))

        for line in list_received:
            print(template.format(*line))

    def option_request_connection(self):
        response = self.sender.request_receive(Message.type_list_user_on_line.value)
        list_received = response.get("list")

        if len(list_received) == 0:
            print("[%s] There are no users waiting for connection"%self.name)
            return

        print("[%s] Request connection, choose one or more users:" % self.name)
        template = "{:^5} - {:^15}|{:^10}|{:^15}|{:^5}|"
        print(template.format("Index", "Nickname", "Status", "IP", "Port"))

        for index, line in enumerate(list_received):
            print(template.format(index, *line))
        
        user_index = input("[%s] Selected users (separate elements by ',')\nAnswer: "%self.name).split(',')

        sender_list = []
        nickname_list = [self.user.nickname]
        for i in user_index:
            selected_user = list_received[int(i)]

            try:
                selected_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                selected_socket.connect((selected_user[2], int(selected_user[3])))
                sender = ClientSender(selected_socket, self.buffer_size)

                sender_list.append(sender)
                nickname_list.append(selected_user[0])
            except ConnectionRefusedError as e:
                print("[%s] Unnable to connect with %s."%(self.name, selected_user[0]))

        request = {
            "type": Message.type_game.value,
            "list": nickname_list
        }
        response = self.sender.request_receive_message(request)
        return sender_list, nickname_list

    def option_wait_connection(self): # Implements the process of listening to a client request to start a game
        self.client_socket.listen(1)
        connection, address = self.client_socket.accept()
        receiver = ClientReceiver(self.user.nickname, connection, address, self.buffer_size, self.user)
        receiver.handle_connection()

    def lobby(self):
        run_menu = True

        while run_menu:
            try:
                option = int(input("[%s] Select an option:\n0 - LIST-USER-ON-LINE\n1 - LIST-USER-PLAYING\n2 - Request connection\n3 - Wait for request\n4 - Exit\nAnswer: "%(self.name)))

                if option == 0: # LIST-USER-ON-LINE
                    self.option_list(Message.type_list_user_on_line.value)
                elif option == 1: # LIST-USER-PLAYING
                    self.option_list(Message.type_list_user_playing.value)
                elif option == 2: # Request an connection with other players
                    sender_list, nickname_list = self.option_request_connection()
                    game = Game(self.user)
                    game.handle_host(sender_list, nickname_list)
                elif option == 3: # Wait for an connection request
                    self.option_wait_connection()
                elif option == 4:
                    run_menu = False
                else: # Invalid option
                        print("[%s] Select an valid option."%self.name)

            except ValueError as e: # Invalid option
                print("[%s] Select an valid option."%self.name)
            except IndexError as e:
                print("[%s] Invalid index option."%self.name)
            
            print(self.menu_string)
