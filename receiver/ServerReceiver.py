import socket
import pickle

from ClientStatus import ClientStatus
from database import DataBase
from Message import Message

class ServerReceiver:
    def __init__(self, name, connection, address, buffer_size):
        self.name = name
        self.connection = connection
        self.address = address
        self.buffer_size = buffer_size
        self.db_con = DataBase()
        self.nick = "LOGGED_OUT"
    
    def print_message(self, menu_name, message_name, message):
        print("[%s] %s\n%s: %s\nAddress: %s" %(self.name, menu_name, message_name, message, self.address))

    def login_account_verification(self, request, address):
        # Implementation the process of verification of the login account and make return True or False if the user is online        
        nickname = request.get("nickname")
        password = request.get("password")

        user = self.db_con.fetch_data(nickname)

        response = {"type": Message.type_login.value}
        if not user:
            response.update({"error": "User not found, check if name was spelled correctly or try creating a new account"})
            response.update({"logged": False})
        elif user[2] != password:
            response.update({"error": "Passwords do not match!"})
            response.update({"logged": False})
        else:
            response.update({"full_name": user[0]})
            response.update({"nickname": nickname})
            response.update({"logged": True})
            print("[%s] User %s login was made successfully, updating status and address" % (self.name, nickname))
            updated = self.db_con.update_connection(nickname, ClientStatus.IDLE.value, "", "")
            self.__handle_authentication(nickname)

            if updated:
                print("[%s] User %s data updated successfully" % (self.name, nickname))

        return response
    
    def create_account_verification(self, request, address):
        # Implementation of the process of profile creation and login on new account if possible
        full_name = request.get("full_name")
        nickname = request.get("nickname")
        password = request.get("password")

        print("address got", address)

        success = self.db_con.save_data(nickname, full_name, password, ClientStatus.IDLE.value, "", "")

        response = {"type": Message.type_login.value}
        if success:
            print("[%s] User %s registration was made successfully" % (self.name, nickname))
            response.update({"full_name": full_name})
            response.update({"nickname": nickname})
            response.update({"logged": True})
            self.__handle_authentication(nickname)
        else:
            response.update({"error": "Error creating user, please check if user already exists or try again"})
            response.update({"logged": False})

        return response

    def __handle_authentication(self, nick):
        self.nick = nick
    
    def handle_menu_login(self):
        print("[%s] %s is connected to the Login Menu."%(self.name, self.address))
        request = pickle.loads(self.connection.recv(self.buffer_size))
        self.print_message("Lobby", "Request", request) # REMOVE debug

        while request.get("type") != Message.type_lobby.value and request.get("type") != Message.type_exit_server.value:
            login_type = request.get("type")

            if login_type == Message.type_login.value:
                response = self.login_account_verification(request, self.address)
            elif login_type == Message.type_create_account.value:
                response = self.create_account_verification(request, self.address)
            else:
                response = "[%s] Unknown type of request." % self.name

            self.print_message("Lobby", "Response", response) # REMOVE debug

            self.connection.send(pickle.dumps(response))
            request = pickle.loads(self.connection.recv(self.buffer_size))
            self.print_message("Lobby", "Request", request) # REMOVE debug
        
        return request
    
    def list_user_on_line(self):
        users = self.db_con.get_by_status(ClientStatus.OFFLINE.value, negated= True)

        users_formatted = []
        for u in users:
            if not (self.address[0]==u[4] and self.address[1]==int(u[5])):
                users_formatted.append([u[1], u[3], u[4], u[5]])

        response = {
            "type": Message.type_list_user_on_line.value,
            "list": users_formatted
        }

        return response

    def list_user_ready_to_play(self):
        users = self.db_con.get_by_status(ClientStatus.READY_TO_CONNECT.value)
        users_playing = self.db_con.get_by_status(ClientStatus.PLAYING.value)

        users_formatted = []
        for u in users + users_playing:
            if not (self.address[0]==u[4] and self.address[1]==int(u[5])):
                users_formatted.append([u[1], u[4], u[5]])
            
        response = {
            "type": Message.type_list_user_ready_to_play.value,
            "list": users_formatted
        }

        return response
    
    def list_user_playing(self):
        # Return a relation list with host player and client player
        users = self.db_con.get_by_status(ClientStatus.PLAYING.value)

        users_formatted = []
        for u in users:
            if not (self.address[0]==u[4] and self.address[1]==int(u[5])):
                users_formatted.append([u[1], u[4], u[5], u[1], u[4], u[5]]) # Not implemented

        response = {
            "type": Message.type_list_user_playing.value,
            "list": users_formatted
        }

        return response

    def handle_game_status(self, request):
        # Update the status of the user
        response = {
            "type": Message.type_game.value,
            "status": request.get("status")
        }
        
        return response

    def __handle_user_ready(self, request):
        ip = request.get("ip")
        port = request.get("port")

        self.db_con.update_connection(self.nick, ClientStatus.READY_TO_CONNECT.value, ip, port)

    def handle_menu_lobby(self):
        print("[%s] %s is connected to the Lobby Menu."%(self.name, self.address))

        request = pickle.loads(self.connection.recv(self.buffer_size))
        self.print_message("Lobby", "Request", request)

        while request.get("type") != Message.type_exit_server.value:
            request_type =  request.get("type")

            if request_type == Message.type_list_user_on_line.value:
                response = self.list_user_on_line()
            elif request_type == Message.type_list_user_playing.value:
                response = self.list_user_playing()
            elif request_type == Message.type_list_user_ready_to_play.value:
                response = self.list_user_ready_to_play()
            elif request_type == Message.type_game.value:
                response = self.handle_game_status(request)
            elif request_type == Message.type_setup_client_ready.value:
                response = self.handle_user_ready(request)
            else:
                response = "[%s] Unknown type of request." % self.name

            self.print_message("Lobby", "Response", response) # REMOVE debug

            self.connection.send(pickle.dumps(response))
            request = pickle.loads(self.connection.recv(self.buffer_size))
            self.print_message("Lobby", "Request", request) # REMOVE debug
        
        return request
    
    def exit_connection(self):
        self.connection.close()
        self.db_con.update_connection(self.nick, ClientStatus.OFFLINE.value, "", "")
        print("[%s] Connection to %s is closed."%(self.name, self.address))

    def handle_connection(self):
        try:
            request = self.handle_menu_login()
            
            if request.get("type") == Message.type_lobby.value: # Verify if the user is logged
                self.handle_menu_lobby()
            
            self.exit_connection()

        except (EOFError, ConnectionResetError) as e:
            print("[%s] ERROR %s lost connection."%(self.name, self.address))
            self.exit_connection()
