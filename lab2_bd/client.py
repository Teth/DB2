from storage import Storage
from message import Message
import json


class Client:
    is_admin = False
    storage_manager = Storage()
    username = None
    p = storage_manager.connection.pubsub()

    def login_user(self, username):
        if self.storage_manager.get_user(username):
            self.username = username
            self.storage_manager.connection.publish('adminJournal', json.dumps({'type': 'logon',
                                                                                'user': username}))
            return True
        else:
            return False

    def register_user(self, username):
        self.storage_manager.add_user(username)

    def create_message(self, message_text, receiver):
        m = Message()
        m.message = message_text
        m.receiver = receiver
        m.sender = self.username
        self.storage_manager.add_message(m)

    def get_message(self, message_hash):
        return self.storage_manager.get_message(message_hash)

    def get_inbox(self, username, n_elem):
        return self.storage_manager.get_messages(username, n_elem)

    def get_spammers(self, n_elem):
        return self.storage_manager.get_spammers(n_elem)

    def get_online(self):
        return self.storage_manager.get_online()

    def logoff(self):
        self.storage_manager.connection.publish('adminJournal', json.dumps({'type': 'logoff',
                                                                            'user': self.username}))
