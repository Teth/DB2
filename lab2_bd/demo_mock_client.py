import sys
from client import Client
user = sys.argv[1]
n_mess = sys.argv[2]
if not n_mess.isalnum():
    print('Mock client NOT initialized')
    quit(0)
n_mess = int(n_mess)
c = Client()
print('Mock client initialized')
c.register_user(user)
c.login_user(user)
for i in range(n_mess):
    print('Sending message')
    c.create_message('Hello world hello num:' + i.__repr__(), 'dan')
c.logoff()
