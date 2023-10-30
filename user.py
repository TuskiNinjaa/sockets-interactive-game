# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class User:
    def __init__(self):
        self.full_name = ""
        self.nickname = ""
        self.logged = False

    def set_full_name(self, full_name):
        self.full_name = full_name

    def set_nickname(self, nickname):
        self.nickname = nickname

    def set_logged(self, logged):
        self.logged = logged

    def set_info(self, user_full_name, nickname, logged):
        self.set_full_name(user_full_name)
        self.set_nickname(nickname)
        self.set_logged(logged)

    def print_info(self):
        print("Full name: %s\nNickname: %s\nLogged: %s" % (self.full_name, self.nickname, self.logged))
