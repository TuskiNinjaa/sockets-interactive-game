from random import sample
from Message import Message
from sender import ClientSender
import pickle

class Game:
    def __init__(self, user):
        self.name = "Fingers Game"
        self.user = user
        self.print_description()

    def print_description(self):
        print("[%s] Lets start the game!"%self.name)
        print("TUTORIAL")

    def handle_player(self, connection, buffer_size):
        request = pickle.loads(connection.recv(buffer_size))
        print("[%s] Request: %s."%(self.name, request))

        while request.get("type") != Message.type_finish_game.value:
            response = {
                "type": Message.type_init_game.value,
                "fingers": self.read_input()
            }
            connection.send(pickle.dumps(response))

            request = pickle.loads(connection.recv(buffer_size))
            print("[%s] Request: %s."%(self.name, request))

            self.print_round_result(request.get("sum"), request.get("looser"), request.get("players"))

            response = {"type": Message.type_init_game.value}
            connection.send(pickle.dumps(response))

            request = pickle.loads(connection.recv(buffer_size))
            print("[%s] Request: %s."%(self.name, request))
            print("%s"%request.get("type"))

    def handle_host(self, sender_list, nickname_list):        
        while len(nickname_list)>1:
            fingers = [] if nickname_list[0]!=self.user.nickname else [self.read_input()]

            for sender in sender_list:
                response = sender.request_receive(Message.type_update_game.value)
                fingers.append(response.get("fingers"))

            sum, looser_index = self.execute_round(fingers)
            nickname_looser = nickname_list.pop(looser_index)

            request = {
                "type": Message.type_update_game.value,
                "sum": sum,
                "players": nickname_list,
                "looser": nickname_looser
            }

            for sender in sender_list:
                response = sender.request_receive_message(request)

            if nickname_looser != self.user.nickname:
                if nickname_list[0]==self.user.nickname:
                    sender = sender_list.pop(looser_index-1)
                else:
                    sender = sender_list.pop(looser_index)
                sender.request(Message.type_finish_game.value)
                sender.close()

            self.print_round_result(sum, nickname_looser, nickname_list)
        
        if nickname_looser!=self.user.nickname: # Host won the game
            self.print_victory()
        else:
            self.print_game_over_player()
            sender_list[0].request(Message.type_finish_game.value)
            sender_list[0].close()

    def print_round_result(self, sum, looser, players):
        print("[%s] Round Result\nPlayers: "%(self.name), end="")
        print(*players)
        print("Sum: %d\nLooser: %s"%(sum, looser))

    def print_game_over_player(self):
        print("[%s] Gave Over. Returning to the Lobby."%self.name)

    def print_game_over_host(self):
        print("[%s] Gave Over. Waiting for the other players."%self.name)

    def print_victory(self):
        print("[%s] You won. Returning to the Lobby."%self.name)

    def read_input(self):
        run_read_input = True
        while run_read_input:
            try:
                finger_num = int(input('Informe a quantia de dedos escolhida: '))
            
                if(finger_num > 10 or finger_num < 0): #Invalid option
                    print("[%s] Error: Type a number between 0 and 10"%self.name)
                else:
                    return(finger_num)
                
            except ValueError:
                print("[%s] Error: Type a number between 0 and 10"%self.name)

    def execute_round(self, fingers):
        sum = 0
        for finger in fingers:
            sum += finger

        return sum, (sum % len(fingers))