from interfaces import MySocket
from database.MyDatabase import MyDatabase

if __name__ == '__main__':
    user = None
    # Verify account, return user
    while user is None:
        print("Email:")
        email = input()
        print("Password (no important passwords):")
        pwd = input()

        mydb = MyDatabase()
        user = mydb.check_account(email, pwd)

        if user is None:
            print("Email or password are wrong. If you are are new user fuck off.\n")

    # Find server (from list)
    servers = mydb.find_available_servers(user["user"])
    for i in range(len(servers)):
        print(f'{i}: {servers[i]["_to"]}')
    print("Choose server:")
    choice_server = servers[int(input())]["_to"]
    print(choice_server)

    # Connect to text and voice sockets
    channels = mydb.find_available_channels(choice_server)
    for i in range(len(channels)):
        print(f'{i}: {channels[i]["name"]} : {channels[i]["type"]}')
    print("Choose channel:")
    choice_index = int(input())
    choice_channel = channels[choice_index]
    print(choice_channel)

    # if choice["active"] is False:
    # find new ip

    # connect to stream
    socket = MySocket.MyClientSocket(user["user"])
    socket.get_channel(str(choice_server) + ":" + str(choice_index))

