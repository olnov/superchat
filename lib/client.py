import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=7675):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.nickname = input("Choose your nickname: ")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                    print("Here - in if")
                else:
                    # Check if the message was sent by the current user
                    if message.startswith(f'[{self.nickname}]:'):
                        print ("HERE!")
                        message = message.replace(f'[{self.nickname}]:', '[me]')
                    print(message, end='', flush=True)
            except:
                print("An error occurred!")
                self.client.close()
                break

    # def receive(self):
    #     while True:
    #         try:
    #             message = self.client.recv(1024).decode('utf-8')
    #             if message == 'NICK':
    #                 self.client.send(self.nickname.encode('utf-8'))
    #             else:
    #                 print(message, end='', flush=True)
    #         except:
    #             print("An error occurred!")
    #             self.client.close()
    #             break

    def write(self):
        while True:
            # message = f'\033[1m[{self.nickname}]:\033[0m\033[92m{input("")}\033[0m'
            message = f'[{self.nickname}]: {input("")}'
            self.client.send(message.encode('utf-8'))

if __name__ == "__main__":
    client = ChatClient()
