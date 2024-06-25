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

    def broadcast(self, message, sender=None):
        colored_message = f'\033[92m{message}\033[0m\n'  # ANSI code for green text
        for client in self.clients:
            if client != sender:
                self.slow_type_send(client, colored_message)

    def handle_client(self, client):
        try:
            # Handshake process
            initial_message = client.recv(1024).decode('utf-8')
            if initial_message == 'Shaken, not stirred':
                client.send('Welcome, Mr. Bond'.encode('utf-8'))
                ack_message = client.recv(1024).decode('utf-8')
                if ack_message == 'ACK':
                    client.send('ACK'.encode('utf-8'))
                    print("Handshake successful with client.")
                else:
                    print("Handshake failed: ACK not received")
                    client.close()
                    return
            else:
                print("Handshake failed: JB phrase not received")
                client.close()
                return

            # Receive and store nickname
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the chat!\n', None)
        except Exception as e:
            print(f"Handshake or nickname error: {e}")
            client.close()
            return

        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message:
                    self.broadcast(message, client)
                else:
                    self.remove(client, nickname)
                    break
            except Exception as e:
                print(f"Communication error: {e}")
                self.remove(client, nickname)
                break

    def remove(self, client, nickname):
        if client in self.clients:
            self.clients.remove(client)
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} left the chat!', None)
            client.close()

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def start(self):
        print('Server started on 7675')
        self.receive()

if __name__ == "__main__":
    server = ChatServer()
    server.start()