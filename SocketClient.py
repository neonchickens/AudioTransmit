import socket
import threading
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


def recieveMessage():
    while True:
        try:
            data = s.recv(1024)
            if len(data) > 0:
                print(str(data))
        except ConnectionResetError:
            print("Server is closed!")
            return;


def sendMessage():
    while True:
        try:
            msg = input()
            print("Sending \"" + msg + "\"")
            s.send(msg.encode())
        except ConnectionResetError:
            print("Server is closed!")
            return;


def recieveMessageAudio():
    streamRecieve = p.open(format=p.get_format_from_width(2),
                           channels=CHANNELS,
                           rate=RATE,
                           output=True)

    while True:
        try:
            data = sAudio.recv(1024)
            streamRecieve.write(data)
        except ConnectionResetError:
            print("Audio server is closed!")
            return;


def sendMessageAudio():
    streamSend = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    while True:
        try:
            data = streamSend.read(CHUNK)
            sAudio.send(data)
        except ConnectionResetError:
            print("Audio server is closed!")
            return;


s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))

sAudio = socket.socket()
portAudio = 12346
sAudio.connect(('127.0.0.1', portAudio))

print("Listening...")
p = pyaudio.PyAudio()
thrListen = threading.Thread(target=recieveMessage, name="thrListen")
thrSpeak = threading.Thread(target=sendMessage, name="thrSpeak")
thrListenAudio = threading.Thread(target=recieveMessageAudio, name="thrListenAudio")
thrSpeakAudio = threading.Thread(target=sendMessageAudio, name="thrSpeakAudio")

thrListen.start()
thrSpeak.start()
thrListenAudio.start()
thrSpeakAudio.start()
