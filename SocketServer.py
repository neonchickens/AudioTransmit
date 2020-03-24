import socket
import threading
import pyaudio


class MyServerSocket:
    port = 12345
    connections = []
    s = None

    def __init__(self):
        pass

    def connect_socket(self):
        pass

    def receive_message(self, conn):
        pass

    def send_message(self, data):
        pass


class SocketText(MyServerSocket):

    def __init__(self):
        self.port = 12345
        self.connections = []
        self.s = socket.socket()
        self.s.bind(('', self.port))

        print("Listening...")
        self.s.listen(5)

        thrJoin = threading.Thread(target=self.connect_socket, name="thrJoin")
        thrJoin.start()

    def connect_socket(self):
        i = 0
        while True:
            conn, addr = self.s.accept()
            print("Connection: " + str(addr))

            i += 1
            conn.send(f"Welcome #{i}".encode())
            self.connections.append(conn)

            thrListen = threading.Thread(target=self.receive_message, args=(conn,), name="thrListen")
            thrListen.start()

    def receive_message(self, conn):
        while True:
            try:
                data = conn.recv(1024)
                if len(data) > 0:
                    print(str(data))
                    self.send_message(data)
            except ConnectionResetError:
                self.connections.remove(conn)
                print(f"{conn} removed")
                conn.close()
                return

    def send_message(self, data):
        for c in self.connections:
            c.send(data)


class SocketAudio(MyServerSocket):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    def __init__(self):
        self.port = 12346
        self.connections = []
        self.s = socket.socket()
        self.s.bind(('', self.port))

        print("Listening...")
        self.s.listen(5)

        thrJoin = threading.Thread(target=self.connect_socket, name="thrJoin")
        thrJoin.start()

    def connect_socket(self):
        i = 0
        while True:
            conn, addr = self.s.accept()
            print("Connection: " + str(addr))

            self.connections.append(conn)

            thrListen = threading.Thread(target=self.receive_message, args=(conn,), name="thrListen")
            thrListen.start()

    def receive_message(self, conn):
        while True:
            try:
                data = conn.recv(1024)
                self.send_message(data)
            except ConnectionResetError:
                self.connections.remove(conn)
                print(f"{conn} removed")
                conn.close()
                return

    def send_message(self, data):
        for c in self.connections:
            c.send(data)
