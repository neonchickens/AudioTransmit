# Program: AudioTransmit
# Module: MyDatabase
# Programmer: Weston Laity
# Desc: Database objects are use to access the data needed without the mess of sql in line

from pyArango.connection import *


class MyDatabase:

    def __init__(self):
        self.conn = Connection(username="wes_pc", password="root")
        self.db = self.conn["AudioTransmit"]

    def check_account(self, email, pwd):
        # checks for matching account credentials
        example = {'email': 'Wes', 'pass': 'pass'}
        query = self.db['account'].fetchByExample(example, batchSize=2, count=True)
        if query.count == 1:
            # returns matching document
            return query[0]
        return None

    def find_available_servers(self, user):
        # checks graph for associated servers
        example = {'_from': 'user/' + str(user)}
        query = self.db['membership'].fetchByExample(example, batchSize=64, count=True)
        # returns all available servers
        return query

    def find_available_channels(self, server):
        # checks selected server channels
        example = {'_id': server}
        query = self.db['server'].fetchByExample(example, batchSize=64, count=True)
        if query.count > 0:
            # returns channels array
            return query[0]["channels"]
        return None

    def find_channel_type(self, server, channel):
        # checks selected channel type
        example = {'_id': server}
        query = self.db['server'].fetchByExample(example, batchSize=2, count=True)
        if query.count > 0:
            # returns channel type
            res = query[0]["channels"][channel]["type"]
            return res
        return None
