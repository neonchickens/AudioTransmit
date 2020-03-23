import socket
import threading
import os


def joinServer():
    i = 0
    while True:
        conn, addr = s.accept()
        print("Connection: " + str(addr))

        i += 1
        conn.send(f"Welcome #{i}".encode())
        connections.append(conn)

        thrListen = threading.Thread(target=recieveMessage, args=(conn,), name="thrListen")
        thrListen.start()


def recieveMessage(conn):
    while True:
        try:
            data = conn.recv(1024)
            if len(data) > 0:
                print(str(data))
                sendMessage(data)
        except ConnectionResetError:
            connections.remove(conn)
            print(f"{conn} removed")
            conn.close()
            return


def sendMessage(data):
    for c in connections:
        c.send(data)


s = socket.socket()
port = 12345
s.bind(('', port))

print("Listening...")
connections = []
s.listen(5)

thrJoin = threading.Thread(target=joinServer, name="thrJoin")
thrJoin.start()

