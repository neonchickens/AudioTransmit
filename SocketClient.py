import socket
import threading


def recieveMessage():
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            print(str(data))


def sendMessage():
    while True:
        msg = input()
        print("Sending \"" + msg + "\"")
        s.send(msg.encode())


s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))

print("Listening...")
thrListen = threading.Thread(target=recieveMessage, name="thrListen")
thrSpeak = threading.Thread(target=sendMessage, name="thrSpeak")

thrListen.start()
thrSpeak.start()
