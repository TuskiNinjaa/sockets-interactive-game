#  sockets-interactive-game

Implementação de jogo interativo usando sockets para o trabalho da matéria de Redes de Computadores - UFMS


*Para rodar:*

 - Primeiro inicie o servidor rodando:

    ```shell
    python3 server.py
    ```
- Após, em outros terminais instancie a quantidade desejada de clientes conectados
    ```shell
    python3 client.py
    ```
  
Enquanto o servidor roda, clientes logam/deslogam e jogos acontecem os dados serão armazenados
em um banco de dados local `storage.db` e um log dump é realizado em `game.log`, onde é possível
acompanhar as atualizações de status dos clientes/jogos