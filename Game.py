import pickle

from Message import Message


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class Game:
    """
        Class used to  handle the game logic
        """
    def __init__(self, user):
        self.name = "FINGERS GAME"
        self.user = user
        self.print_description()

    def print_description(self):
        print("[%s] Lets start the game!" % self.name)
        print("TUTORIAL:\nShow a number from 0 to 10, if the counter stops on you, you are out of the game.")

    """
        Method used to handle the game as a player
        this waits for the host messages (P2P connection)
        to update the game stages till the end
        """
    def handle_player(self, connection, buffer_size):
        print("[%s] Waiting for your turn." % self.name)
        request = pickle.loads(connection.recv(buffer_size))

        while request.get("type") != Message.type_finish_game.value:
            response = {
                "type": Message.type_update_game.value,
                "fingers": self.read_input()
            }
            connection.send(pickle.dumps(response))

            result = pickle.loads(connection.recv(buffer_size))

            self.print_round_result(result.get("sum"), result.get("loser"), result.get("players"))

            response = {"type": Message.type_update_game.value}
            connection.send(pickle.dumps(response))

            request = pickle.loads(connection.recv(buffer_size))
            if request.get("type") != Message.type_finish_game.value:
                print("[%s] Waiting for your turn." % self.name)

        request_to_server = {"type": Message.type_update_game.value}
        if result.get("loser") == self.user.nickname:
            request_to_server.update({"is_loser": True})
        else:
            request_to_server.update({"is_loser": False})

        return request_to_server

    """
            Method used to handle the game as a host
            this sends messages for the players (P2P connection)
            to update the game stages till the end
            """
    def handle_host(self, sender_list, nickname_list):
        while len(nickname_list) > 1:
            fingers = [] if nickname_list[0] != self.user.nickname else [self.read_input()]

            for sender in sender_list:
                response = sender.request_receive(Message.type_update_game.value)
                fingers.append(response.get("fingers"))

            sum, loser_index = self.execute_round(fingers)
            nickname_loser = nickname_list.pop(loser_index)

            request = {
                "type": Message.type_update_game.value,
                "sum": sum,
                "players": nickname_list,
                "loser": nickname_loser
            }

            for sender in sender_list:
                response = sender.request_receive_message(request)

            if nickname_loser != self.user.nickname:
                if nickname_list[0] == self.user.nickname:
                    sender = sender_list.pop(loser_index - 1)
                else:
                    sender = sender_list.pop(loser_index)
                sender.request(Message.type_finish_game.value)
                sender.close()
            else:
                self.print_game_over_host()

            self.print_round_result(sum, nickname_loser, nickname_list)

        request_to_server = {"type": Message.type_finish_game.value}
        if nickname_list[0] == self.user.nickname:  # Host won the game
            self.print_victory()
            request_to_server.update({"is_loser": False})
            request_to_server.update({"winner": self.user.nickname})
        else:  # Host lost the game
            self.print_game_over_player()
            (sender_list[0]).request(Message.type_finish_game.value)
            (sender_list[0]).close()
            request_to_server.update({"is_loser": True})
            request_to_server.update({"winner": nickname_list[0]})
        return request_to_server

    def print_round_result(self, sum, loser, players):
        print("[%s] Round Result\nPlayers: " % (self.name), end="")
        print(*players)
        print("Sum: %d\nLoser: %s" % (sum, loser))

    def print_game_over_player(self):
        print("[%s] Gave Over. Returning to the Lobby." % self.name)

    def print_game_over_host(self):
        print("[%s] Gave Over. Waiting for the other players." % self.name)

    def print_victory(self):
        print("[%s] You won. Returning to the Lobby." % self.name)

    """
            Method used to handle player input in the game
            """
    def read_input(self):
        run_read_input = True
        while run_read_input:
            try:
                finger_num = int(input('Show your fingers [0, 10]: '))

                if (finger_num > 10 or finger_num < 0):  # Invalid option
                    print("[%s] Error: Type a number between 0 and 10" % self.name)
                else:
                    return (finger_num)

            except ValueError:
                print("[%s] Error: Type a number between 0 and 10" % self.name)

    def execute_round(self, fingers):
        sum = 0
        for finger in fingers:
            sum += finger

        return sum, (sum % len(fingers))
