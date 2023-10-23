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
        print("Handling player")
        request = pickle.loads(connection.recv(buffer_size))
        print("[%s] Request: %s."%(self.name, request))

        while request.get("type") != Message.type_lobby.value:
            response = {
                "type": Message.type_game.value,
                "fingers": self.read_input()
            }
            connection.send(pickle.dumps(response))

            request = pickle.loads(connection.recv(buffer_size))
            print("[%s] Request: %s."%(self.name, request))

            response = {"type": Message.type_game.value}
            connection.send(pickle.dumps(response))

            request = pickle.loads(connection.recv(buffer_size))
            print("[%s] Request: %s."%(self.name, request))
            print("%s"%request.get("type"))


    def handle_host(self, sender_list, nickname_list):        
        while len(sender_list)>0:
            fingers = [] if nickname_list[0]!=self.user.nickname else [self.read_input()]

            for sender in sender_list:
                response = sender.request_receive(Message.type_game.value)
                fingers.append(response.get("fingers"))

            print(fingers)
            sum, looser_index = self.execute_round(fingers)
            print("[%s] Sum: %s. Looser: %s"%(self.name, sum, nickname_list[looser_index]))

            request = {
                "type": Message.type_game,
                "sum": sum,
                "players": nickname_list,
                "looser": nickname_list[looser_index]
            }

            for sender in sender_list:
                response = sender.request_receive_message(request)

            nickname = nickname_list.pop(looser_index)
            if nickname != self.user.nickname:
                if nickname_list[0]==self.user.nickname:
                    sender = sender_list.pop(looser_index-1)
                else:
                    sender = sender_list.pop(looser_index)

                sender.request(Message.type_lobby.value)

            print(nickname)


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