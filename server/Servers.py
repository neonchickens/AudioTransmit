# Program: AudioTransmit
# Module: Servers
# Programmer: Weston Laity
# Desc: This is where the server starts the program. We just start up the server socket which will handle user
#       connections and communications

from interfaces import MySocket

if __name__ == '__main__':
    # Put servers up on request, put them down when not in use

    # A user will join and want to see their servers
    # The list of servers he's in is returned
    # They chooses a server and is presented with the channels/sockets
    # We boot up sockets as they choose them
    sockets = MySocket.MyServerSocket()
