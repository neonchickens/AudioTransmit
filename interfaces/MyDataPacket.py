# Program: AudioTransmit
# Module: MyDataPacket
# Programmer: Weston Laity
# Desc: Data packet we use to standardize communication between client and server. All communication is expected to be
#       sent in a packet.

import pickle


class MyDataPacket:
    data = {}

    def __init__(self, packet):
        self.data = {"_from": None,
                     "_to": None,
                     "command": None,
                     "flags": None,
                     "parameters": None
                     }
        if packet is not None:
            try:
                # unpacks binary to packet object
                unpacked = pickle.loads(packet)
                for k in self.data.keys():
                    if unpacked.data[k] is not None:
                        self.data[k] = unpacked.data[k]
            except pickle.UnpicklingError:
                raise EOFError()

    def get_data(self):
        return self.data

    @staticmethod
    def format(mdp):
        # turns packet into binary for transport
        return pickle.dumps(mdp)
