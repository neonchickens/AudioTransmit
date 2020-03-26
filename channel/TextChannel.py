# Program: AudioTransmit
# Module: TextChannel
# Programmer: Weston Laity
# Desc: Provides an implementation of MyChannel's ServerChannel and ClientChannel. This allows for the user to send
#       text messages back and forth through the channel and console chat

from interfaces import MyChannel
import threading


class ServerChannel(MyChannel.ServerChannel):

    def receive(self, packet):
        # retransmit text packets
        self.send_packet(packet)


class ClientChannel(MyChannel.ClientChannel):

    def __init__(self, id, userId, server):
        super().__init__(id, userId, server)

        # continuously record new user text
        thrWriteText = threading.Thread(target=self.write_text, name="thrWriteText")
        thrWriteText.start()

    def receive(self, packet):
        # print in chat
        if packet.get_data()["command"] is not None:
            print(str(packet.get_data()["command"]))

    def write_text(self):
        # continuously record new user text
        while True:
            msg = input()
            self.send(msg)
