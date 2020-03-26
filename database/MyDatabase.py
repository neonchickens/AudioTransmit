from pyArango.connection import *


class MyDatabase:

    def __init__(self):
        self.conn = Connection(username="wes_pc", password="root")
        self.db = self.conn["AudioTransmit"]

    def check_account(self, email, pwd):
        example = {'email': 'Wes', 'pass': 'pass'}
        query = self.db['account'].fetchByExample(example, batchSize=2, count=True)
        if query.count == 1:
            return query[0]
        return None

    def find_available_servers(self, user):
        example = {'_from': 'user/' + str(user)}
        query = self.db['membership'].fetchByExample(example, batchSize=64, count=True)
        return query

    def find_available_channels(self, server):
        example = {'_id': server}
        query = self.db['server'].fetchByExample(example, batchSize=64, count=True)
        if query.count > 0:
            return query[0]["channels"]
        return None

    def find_channel_type(self, server, channel):
        example = {'_id': server}
        query = self.db['server'].fetchByExample(example, batchSize=2, count=True)
        if query.count > 0:
            res = query[0]["channels"][channel]["type"]
            return res
        return None
