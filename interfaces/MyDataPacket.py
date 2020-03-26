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
        return pickle.dumps(mdp)
