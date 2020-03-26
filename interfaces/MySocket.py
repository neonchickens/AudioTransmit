from channel import *
import socket
import threading
from os import listdir
from os.path import isfile, join
from interfaces import MyDataPacket
from database import MyDatabase


class MySocket:
    ip = '127.0.0.1'
    port = 21250
    socket = None
    channels = {}  # id: ref
    channelTypes = None
    isServer = False

    def __init__(self):
        self.socket = socket.socket()
        self.load_channel_types()

    def load_channel_types(self):
        self.channelTypes = {}
        path = "../channel/"
        types = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".py") and not f.startswith("__")]
        for t in types:
            t = t.split(".")[0]
            self.channelTypes[t] = globals()[t]

    def get_channel(self, id):
        pass

    def receive_packet(self):
        pass


class MyClientSocket(MySocket):
    ip = '127.0.0.1'
    id = None
    lock = None

    def __init__(self, id):
        super().__init__()
        self.socket.connect((self.ip, self.port))
        self.id = id

        self.lock = threading.Lock()

        thrReceivePacket = threading.Thread(target=self.receive_packet, name="thrReceivePacket")
        thrReceivePacket.start()

    def receive_packet(self):
        data = []
        packet = None
        while True:
            try:
                packet = self.socket.recv(4096)
                data.append(packet)
                if len(packet) > 0:
                    mdp = MyDataPacket.MyDataPacket(b"".join(data))
                    data = []
                    self.get_channel(mdp.get_data()["_from"]).receive(mdp)
            except ConnectionResetError:
                print("Server is closed!")
                return
            except EOFError:
                packet = packet

    def get_channel(self, channelId):
        with self.lock:
            if channelId not in self.channels:
                mydb = MyDatabase.MyDatabase()
                type = mydb.find_channel_type(channelId.split(":")[0], int(channelId.split(":")[1]))
                mdp = MyDataPacket.MyDataPacket(None)
                mdp.get_data()["_from"] = self.id
                mdp.get_data()["_to"] = channelId
                mdp.get_data()["command"] = None

                self.socket.send(MyDataPacket.MyDataPacket.format(mdp))
                self.channels[channelId] = self.channelTypes[type].ClientChannel(channelId, self.id, self.socket)
        return self.channels[channelId]


class MyServerSocket(MySocket):
    user2conn = {}  # id: conn

    def __init__(self):
        super().__init__()
        self.socket.bind(('', self.port))

        print("Listening...")
        self.socket.listen(5)

        thrReceiveConnection = threading.Thread(target=self.receive_connection, name="thrReceiveConnection")
        thrReceiveConnection.start()

    def receive_connection(self):
        while True:
            conn, addr = self.socket.accept()
            print("Connection: " + str(addr))

            thrReceiveMessage = threading.Thread(target=self.receive_message, args=(conn,), name="thrReceiveMessage")
            thrReceiveMessage.start()

    def receive_message(self, conn):
        data = []
        packet = None
        while True:
            try:
                packet = conn.recv(4096)
                data.append(packet)
                if len(packet) > 0:
                    mdp = MyDataPacket.MyDataPacket(b"".join(data))
                    data = []
                    self.user2conn[mdp.get_data()["_from"]] = conn
                    chan = self.get_channel(mdp.get_data()["_to"])
                    if mdp.get_data()["_from"] not in chan.get_connections():
                        chan.get_connections()[mdp.get_data()["_from"]] = conn
                    chan.receive(mdp)
            except ConnectionResetError:
                print(f"{conn} removed")
                conn.close()
                return
            except EOFError:
                packet = packet

    def get_channel(self, id):
        if id not in self.channels:
            mydb = MyDatabase.MyDatabase()
            type = mydb.find_channel_type(id.split(":")[0], int(id.split(":")[1]))
            self.channels[id] = self.channelTypes[type].ServerChannel(id, {})
            print(f"Channel {id} created!")
        return self.channels[id]
