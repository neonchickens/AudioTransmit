from interfaces import MySocket

if __name__ == '__main__':
    # Put servers up on request, put them down when not in use

    # A user will join and want to see their servers
    # The list of servers he's in is returned
    # They chooses a server and is presented with the channels/sockets
    # We boot up sockets as they choose them
    sockets = MySocket.MyServerSocket()
