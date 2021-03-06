# Program: AudioTransmit
# Module: MyChannel
# Programmer: Weston Laity
# Desc: Provides the interface of MyChannel's ServerChannel and ClientChannel. This allows for the creation of abstract
#       objects for server communication

from interfaces import MyDataPacket


class MyChannel:
    # General channel structure (all channels will inherit from these)
    id = None

    def __init__(self, id):
        self.id = id

    def receive(self, data):
        pass

    def send(self, data):
        # start --> send (data) --> send_packet(packaged_data) --> destination
        mdp = MyDataPacket.MyDataPacket(None)
        mdp.get_data()["command"] = data
        self.send_packet(mdp)

    def send_packet(self, packet):
        pass


class ServerChannel(MyChannel):
    # General channel structure for servers

    user2conn = {}  # id: conn

    def __init__(self, id, connections):
        super().__init__(id)
        self.user2conn = connections

    def get_connections(self):
        return self.user2conn

    def add_connections(self, user, conn):
        self.user2conn[user] = conn

    def receive(self, data):
        print(str(data))

    def send_packet(self, packet):
        remove = []
        for k in self.user2conn.keys():
            packet.get_data()["_to"] = k
            packet.get_data()["_from"] = self.id
            try:
                self.user2conn[k].send(MyDataPacket.MyDataPacket.format(packet))
            except OSError:
                remove.append(k)

        for k in remove:
            self.user2conn.pop(k)


class ClientChannel(MyChannel):
    # General channel structure for clients

    server = None
    userId = None

    def __init__(self, id, userId, server):
        super().__init__(id)
        self.userId = userId
        self.server = server

    def send_packet(self, packet):
        packet.get_data()["_to"] = self.id
        packet.get_data()["_from"] = self.userId
        self.server.send(MyDataPacket.MyDataPacket.format(packet))
