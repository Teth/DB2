from time import sleep

from storage import Storage
import json


class Journal:
    logging = None

    def __init__(self, logger=True):
        self.s = Storage()
        self.p = self.s.connection.pubsub()
        self.logging = logger
        self.p.subscribe('adminJournal')
        print('Journal started')

    def start(self):
        self.output_logging()

    def output_logging(self):
        RUN = True
        while RUN:

            message = self.p.get_message()
            if message and message['type'] == 'message':
                message = json.loads(message['data'])
                message_type = message['type']
                if message_type == 'spam':
                    self.db_append_spammer(message['user'])
                    if self.logging:
                        print('Detected SPAM from {}'.format(message['user']))
                if message_type == 'logon':
                    self.logon()
                    if self.logging:
                        print('User {} is now online'.format(message['user']))
                if message_type == 'logoff':
                    self.logoff()
                    if self.logging:
                        print('User {} is now offline'.format(message['user']))
            sleep(0.01)

    def db_append_spammer(self, username):
        self.s.inc_spammer(username)

    def logoff(self):
        return self.s.dec_online()

    def logon(self):
        return self.s.inc_online()
