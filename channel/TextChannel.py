from interfaces import MyChannel
import threading


class ServerChannel(MyChannel.ServerChannel):

    def receive(self, packet):
        self.send_packet(packet)


class ClientChannel(MyChannel.ClientChannel):

    def __init__(self, id, userId, server):
        super().__init__(id, userId, server)
        thrWriteText = threading.Thread(target=self.write_text, name="thrWriteText")
        thrWriteText.start()

    def receive(self, packet):
        if packet.get_data()["command"] is not None:
            print(str(packet.get_data()["command"]))

    def write_text(self):
        while True:
            msg = input()
            self.send(msg)
