import redis
import hashlib
import time

hasher = hashlib.sha1()


redis_host = "localhost"
redis_port = 6379
redis_password = ""

users_namespace = 'users'
message_namespace = 'messages'
inbox_namespace = 'inbox'
spammer_namespace = 'spammers'
message_queue_name = 'queue'


class MessageState:
    S_CREATED = 'CREATED'
    S_INQ = 'IN QUEUE'
    S_CHECK = 'CHECKING FOR SPAM'
    S_SPAM = 'SPAM'
    S_SENT = 'SENT'
    S_RECEIVED = 'RECEIVED'


def create_user_namespace_string(name):
    return users_namespace + ':' + name


def create_message_namespace_string(user):
    return message_namespace + ':' + user


def create_inbox_namespace_string(user):
    return inbox_namespace + ':' + user


def create_spammer_namespace_string(user):
    return spammer_namespace + ':' + user


class Storage:
    connection = None

    def __init__(self):
        try:
            self.connection = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password,
                                                decode_responses=True)
        except Exception as e:
            print(e)

    # USER
    # key - name
    #

    def add_user(self, name):
        return self.connection.set(create_user_namespace_string(name), 0, nx=True)

    def get_user(self, name):
        return self.connection.get(create_user_namespace_string(name))

    # MESSAGE hash
    # message
    # status
    # sender
    # receiver

    def add_message(self, message):
        hasher.update(str(time.time()).encode('utf-8'))
        message_dict = {"Message": message.message, "Status": MessageState.S_CREATED, "Sender": message.sender,
                        "Receiver": message.receiver}
        hashcode = hasher.hexdigest()[:8]
        self.connection.hmset(hashcode, message_dict)
        self.push_message_hash_to_queue(hashcode)
        return self.connection.lpush(create_message_namespace_string(message.sender), hashcode)

    def update_message_state(self, hashcode, message_status):
        return self.connection.hset(hashcode, "Status", message_status)

    def get_message(self, hashcode):
        return self.connection.hgetall(hashcode)

    def get_message_receiver(self, hashcode):
        return self.connection.hget(hashcode, "Receiver")

    def push_message_hash_to_queue(self, hashcode):
        return self.connection.rpush(message_queue_name, hashcode)

    def get_message_hash_from_queue(self):
        return self.connection.lpop(message_queue_name)

    def send_message(self, hashcode, receiver):
        return self.connection.lpush(create_inbox_namespace_string(receiver), hashcode)

    def get_messages(self, receiver, n_elem):
        return self.connection.lrange(create_inbox_namespace_string(receiver), 0, n_elem)

    def inc_spammer(self, username):
        return self.connection.zincrby(spammer_namespace, 1, username)

    def inc_online(self):
        return self.connection.incr('online')

    def dec_online(self):
        return self.connection.decr('online')

    def get_online(self):
        return self.connection.get('online')

    def get_spammers(self, n_elem):
        return self.connection.zrange(spammer_namespace, 0, n_elem, withscores=True, desc=True)
