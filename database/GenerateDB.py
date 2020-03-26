from pyArango.connection import *
import pyArango.collection as COL
import pyArango.validation as VAL
from pyArango.theExceptions import ValidationError
import types


class Account(COL.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": True,
            "type": "string"
        }
    }

    _fields = {
        'email': COL.Field(validators=[VAL.NotNull()]),
        'password': COL.Field(validators=[VAL.NotNull()]),
        'user': COL.Field(validators=[VAL.NotNull()])
    }


class User(COL.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
            "increment": 1,
            "offset": 0,
        }
    }

    _fields = {
        'username': COL.Field(validators=[VAL.NotNull()])
    }


class Server(COL.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
            "increment": 1,
            "offset": 0,
        }
    }

    _fields = {
        'name': COL.Field(validators=[VAL.NotNull()]),
        'owner': COL.Field(validators=[VAL.NotNull()]),
        'channels': COL.Field(),
        'roles': COL.Field(),
        'ip': COL.Field(validators=[VAL.NotNull()])
    }


class Channel(COL.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
            "increment": 1,
            "offset": 0,
        }
    }

    _fields = {
        'name': COL.Field(validators=[VAL.NotNull()]),
        'type': COL.Field(validators=[VAL.NotNull()]),
        'active': COL.Field(validators=[VAL.NotNull()]),
        'port': COL.Field()
    }


if __name__ == '__main__':
    conn = Connection(username="wes_pc", password="root")
    db = conn["AudioTransmit"]
    print(db['user']['161896'])
    # accounts = db.createCollection(name="account", type=Account)
    # users = db.createCollection(name="user", type=User)
    #
    # acts = [['Wes', 'pass', 'neonchickens'], ['Kat', 'meow', 'KatsAreBetter'], ['Dinah', 'fish', 'GrumpyCat'],
    #         ['Jonas', 'beer', 'Jojo']]
    # for i in range(len(acts)):
    #
    #     a = accounts.createDocument()
    #     u = users.createDocument()
    #
    #     # Save and gen key
    #     u['username'] = acts[i][2]
    #     u.save()
    #     a['user'] = u._key
    #
    #     a['email'] = acts[i][0]
    #     a['pass'] = acts[i][1]
    #     a._key = acts[i][0]
    #     a.save()

    server = db.createCollection(name="server", type=Server)
    servs = [['Sharkult', 'user/161896', [{'name': 'Holy Text', 'type': 'text', 'active': False},
                                          {'name': 'Holy Praises', 'type': 'voice', 'active': False}]],
             ['Haunted Mansion', 'user/161905', [{'name': 'Lease Terms', 'type': 'text', 'active': False},
                                                 {'name': 'Beer List', 'type': 'text', 'active': False},
                                                 {'name': 'Stairway Chatter', 'type': 'voice', 'active': False}]]]
    for i in range(len(servs)):
        s = server.createDocument()
        s['name'] = servs[i][0]
        s['owner'] = servs[i][1]
        s['channels'] = servs[i][2]
        s['ip'] = '127.0.0.1'
        s.save()
    #
    # res = db.AQLQuery("for c in user return c", rawResults=False)
    # for i in res:
    #     print(str(i))


