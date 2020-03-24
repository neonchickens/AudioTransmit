import socket
import threading
import os
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output2.wav"


def joinServer():
    i = 0
    while True:
        conn, addr = s.accept()
        print("Connection: " + str(addr))

        connections.append(conn)

        thrListen = threading.Thread(target=recieveMessageAudio, args=(conn,), name="thrListen")
        thrListen.start()


def recieveMessageAudio(conn):
    while True:
        try:
            data = conn.recv(1024)
            sendMessageAudio(data)
        except ConnectionResetError:
            connections.remove(conn)
            print(f"{conn} removed")
            conn.close()
            return


def sendMessageAudio(data):
    for c in connections:
        c.send(data)


s = socket.socket()
port = 12346
s.bind(('', port))

print("Listening...")
connections = []
s.listen(5)

thrJoin = threading.Thread(target=joinServer, name="thrJoin")
thrJoin.start()

