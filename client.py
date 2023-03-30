import socket
import threading


class Client:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.name = input("Enter your name: ")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.name.encode())
        welcome_message = self.client_socket.recv(1024).decode()
        print(welcome_message)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except:
                print("Connection closed")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            message = input()
            self.client_socket.send(message.encode())
            if message == "quit":
                self.client_socket.close()
                break

if __name__ == "__main__":
    client = Client()
    receive_thread = threading.Thread(target=client.receive_messages)
    receive_thread.start()
    send_thread = threading.Thread(target=client.send_messages)
    send_thread.start()

