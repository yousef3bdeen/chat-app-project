import socket
import threading

class Server:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

    def handle_client(self, conn, addr):
        name = conn.recv(1024).decode()
        welcome_message = f"Welcome, {name}! Type 'list' to see all connected clients or 'devices' to see all connected devices."
        conn.send(welcome_message.encode())
        message = f"{name} has joined the chat!"
        self.broadcast(message, conn)
        while True:
            try:
                message = conn.recv(1024).decode()
                if message == "quit":
                    conn.close()
                    self.clients.remove(conn)
                    leave_message = f"{name} has left the chat."
                    self.broadcast(leave_message, conn)
                    print(f"Connection closed by {addr}")
                    break
                elif message == "list":
                    self.list_all_clients(conn)
                elif message == "devices":
                    self.list_all_devices(conn)
                else:
                    self.broadcast(f"{name}: {message}", conn)
            except:
                conn.close()
                self.clients.remove(conn)
                leave_message = f"{name} has left the chat unexpectedly."
                self.broadcast(leave_message, conn)
                print(f"Connection closed unexpectedly by {addr}")
                break

    def list_all_clients(self, conn):
        clients_list = "\n".join([f"- {client.getpeername()[0]}:{client.getpeername()[1]}" for client in self.clients])
        conn.send(clients_list.encode())

    def list_all_devices(self, conn):
        devices = [(self.host, self.port)] + [client.getpeername() for client in self.clients]
        devices_list = "\n".join([f"- {device[0]}:{device[1]}" for device in devices])
        conn.send(devices_list.encode())

    def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                client.send(message.encode())

    def start(self):
        while True:
            conn, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = Server()
    server.start()
