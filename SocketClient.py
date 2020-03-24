import socket
import threading
import pyaudio


class MyClientSocket:
    port = 12345
    ip = '127.0.0.1'
    connections = []
    s = None

    def __init__(self):
        pass

    def receive_message(self):
        pass

    def send_message(self):
        pass


class SocketText(MyClientSocket):

    def __init__(self):
        self.port = 12345
        self.s = socket.socket()
        self.s.connect((self.ip, self.port))

        thrListen = threading.Thread(target=self.receive_message, name="thrListen")
        thrSpeak = threading.Thread(target=self.send_message, name="thrSpeak")

        thrListen.start()
        thrSpeak.start()

    def receive_message(self):
        while True:
            try:
                data = self.s.recv(1024)
                if len(data) > 0:
                    print(str(data))
            except ConnectionResetError:
                print("Server is closed!")
                return

    def send_message(self):
        while True:
            try:
                msg = input()
                print("Sending \"" + msg + "\"")
                self.s.send(msg.encode())
            except ConnectionResetError:
                print("Server is closed!")
                return


class SocketAudio(MyClientSocket):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = None

    def __init__(self):
        self.port = 12346
        self.s = socket.socket()
        self.s.connect((self.ip, self.port))

        self.p = pyaudio.PyAudio()

        thrListen = threading.Thread(target=self.receive_message, name="thrListen")
        thrSpeak = threading.Thread(target=self.send_message, name="thrSpeak")

        thrListen.start()
        thrSpeak.start()

    def receive_message(self):
        streamRecieve = self.p.open(format=self.p.get_format_from_width(2),
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    output=True)

        while True:
            try:
                data = self.s.recv(1024)
                streamRecieve.write(data)
            except ConnectionResetError:
                print("Audio server is closed!")
                return

    def send_message(self):
        streamSend = self.p.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK)
        while True:
            try:
                data = streamSend.read(self.CHUNK)
                self.s.send(data)
            except ConnectionResetError:
                print("Audio server is closed!")
                return
