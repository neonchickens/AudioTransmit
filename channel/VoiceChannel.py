# Program: AudioTransmit
# Module: VoiceChannel
# Programmer: Weston Laity
# Desc: Provides an implementation of MyChannel's ServerChannel and ClientChannel. This allows for the user to send
#       voice audio back and forth through the channel

from interfaces import MyChannel
import threading
import pyaudio


class ServerChannel(MyChannel.ServerChannel):

    def receive(self, packet):
        # retransmit audio packets
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

        # continuously record new user audio
        thrRecordAudio = threading.Thread(target=self.record_audio, name="thrRecordAudio")
        thrRecordAudio.start()

    def receive(self, packet):
        # play through audio stream
        if packet.get_data()["command"] is not None:
            self.audioOutput.write(packet.get_data()["command"])

    def record_audio(self):
        streamSend = self.p.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK)
        while True:
            # continuously record new user audio
            try:
                data = streamSend.read(self.CHUNK)
                self.send(data)
            except ConnectionResetError:
                print("Audio server is closed!")
                return
