import socket
import threading
import argparse

class ChatClient:
    def __init__(self, host='chat.novlab.org', port=7675):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
        # James Bond handshake process
        try:
            self.client.send('Shaken, not stirred'.encode('utf-8'))
            response = self.client.recv(1024).decode('utf-8')
            if response == 'Welcome, Mr. Bond':
                self.client.send('ACK'.encode('utf-8'))
                final_ack = self.client.recv(1024).decode('utf-8')
                if final_ack == 'ACK':
                    print("Handshake successful with server.")
                else:
                    self.client.close()
                    return
            else:
                self.client.close()
                return
        except:
            self.client.close()
            return

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
                else:
                    print(message, end='', flush=True)
            except:
                print("An error occurred!")
                self.client.close()
                break


    def write(self):
        while True:
            message = f'\033[1m[{self.nickname}]:\033[0m\033[92m{input("")}\033[0m'
            print (message)
            self.client.send(message.encode('utf-8'))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SuperChat Client")
    parser.add_argument('host', help="The server host to connect to")
    parser.add_argument('port', type=int, help="The server port to connect to")
    args = parser.parse_args()

    client = ChatClient(args.host, args.port)