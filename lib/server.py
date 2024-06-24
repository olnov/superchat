import socket
import threading
import time

class ChatServer:
    def __init__(self, host='0.0.0.0', port=7675):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

    def slow_type_send(self, client, message):
        for char in message:
            client.send(char.encode('utf-8'))
            time.sleep(0.05)  # Adjust the delay to change typing speed

    def broadcast(self, message):
        colored_message = f'\033[92m{message}\033[0m\n'  # ANSI code for green text
        for client in self.clients:
            self.slow_type_send(client, colored_message)

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} left the chat!')
                self.nicknames.remove(nickname)
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the chat!')
            client.send('Connected to the server!\n'.encode('utf-8'))

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def start(self):
        print('\033[1m'+'Server started on port [7675]'+'\033[0m')
        self.receive()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
