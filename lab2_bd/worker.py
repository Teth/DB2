import os
import random
import json
from time import sleep
from storage import Storage, MessageState


class Worker:
    spam_percentage = 0.3
    working = False
    storage_manager = None

    def __init__(self):
        self.storage_manager = Storage()
        print('Initialized worker ' + os.getpid().__repr__())

    def is_spam(self, message):
        sleep(random.random() * 3)
        is_spam = random.choices([True, False], [self.spam_percentage, 1 - self.spam_percentage], k=1)
        return is_spam[0]

    def analyze_next_message_for_spam(self):
        message_hash = self.storage_manager.get_message_hash_from_queue()
        if message_hash:
            self.storage_manager.update_message_state(message_hash, MessageState.S_CHECK)
            message = self.storage_manager.get_message(message_hash)
            is_spam = self.is_spam(message)
            if is_spam:
                print('Spam Detected')
                self.storage_manager.connection.publish('adminJournal', json.dumps({'type': 'spam',
                                                                                    'user': message['Sender']}))
                self.storage_manager.update_message_state(message_hash, MessageState.S_SPAM)
            else:
                receiver = self.storage_manager.get_message_receiver(message_hash)
                self.storage_manager.update_message_state(message_hash, MessageState.S_SENT)
                self.storage_manager.send_message(message_hash, receiver)


class Worker_unit:
    def __init__(self):
        self.worker = Worker()

    def start(self):
        while True:
            self.worker.analyze_next_message_for_spam()
            sleep(0.01)

