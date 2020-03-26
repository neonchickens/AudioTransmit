from interfaces import MyChannel
import threading
import pyaudio


class ServerChannel(MyChannel.ServerChannel):

    def receive(self, packet):
        self.send_packet(packet)


class ClientChannel(MyChannel.ClientChannel):

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    p = None

    def __init__(self, id, userId, server):
        super().__init__(id, userId, server)
        print("Audio started!")
        self.p = pyaudio.PyAudio()
        self.audioOutput = self.p.open(format=self.p.get_format_from_width(2),
                                       channels=self.CHANNELS,
                                       rate=self.RATE,
                                       output=True)
        thrRecordAudio = threading.Thread(target=self.record_audio, name="thrRecordAudio")
        thrRecordAudio.start()

    def receive(self, packet):
        if packet.get_data()["command"] is not None:
            self.audioOutput.write(packet.get_data()["command"])

    def record_audio(self):
        streamSend = self.p.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK)
        while True:
            try:
                data = streamSend.read(self.CHUNK)
                self.send(data)
            except ConnectionResetError:
                print("Audio server is closed!")
                return
