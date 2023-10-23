from random import sample

class Game:
    def __init__(self, player):
        self.player = player

    def initialize(self):
        print(
            "Vamos iniciar o jogo agora! \n"
            + "Para jogar, você deve informar o número de dedos levantados e então será realizada uma contagem para ver quem será eliminado. O último que sobrar ganha."
            )

    def read_input(self):
        run_read_input = True
        while run_read_input:
            try:
                finger_num = int(input('Informe a quantia de dedos escolhida: '))
            
                if(finger_num > 10 or finger_num < 0): #Invalid option
                    finger_num = int(input('Error, type a number between 0 and 10: '))
                else:
                    return(finger_num)
                
            except ValueError:
                print("Error. Type a number between 0 and 10")

    def execute_round(self, lista):
        self.lista = lista
        tam_n = len(lista)
        soma_t = 0

        for item in lista:
            soma_t += item 

        if(soma_t == 0):
            posicao = 0
            return(posicao)
        
        else:
            posicao = 0
            contador = 1
            while(contador != soma_t):
                if(posicao < tam_n):
                    if(posicao == (tam_n-1)):
                        posicao = 0
                    else:
                        posicao += 1
                
            contador += 1
        
            return(posicao)