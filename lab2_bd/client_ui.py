import sys
from client import Client
from PyInquirer import prompt
import views
running = True
is_admin = False

if len(sys.argv) > 1:
    is_admin = sys.argv[1] == 'admin'

operations = None
if is_admin:
    operations = views.operations_admin
else:
    operations = views.operations_user

c = Client()
not_logged_in = True
while not_logged_in:
    un = prompt(views.input_name)['value']
    if c.login_user(un):
        not_logged_in = False
    else:
        print('You are not registered')
        if prompt(views.choice_register)['value'] == 'Yes':
            c.register_user(un)
            c.login_user(un)
            not_logged_in = False

while running:
    op = prompt(operations)['operation']
    if op == 'Create message':
        message = prompt(views.input_message)['value']
        reciever = prompt(views.input_receiver)['value']
        c.create_message(message, reciever)
    if op == 'View Inbox':
        messages = c.get_inbox(c.username, 10)
        if messages:
            message_list = []
            for hashcode in messages:
                mess = c.get_message(hashcode)
                message_dict = {'message_str': mess['Sender'] + ' ' + mess['Message'][:8] + '...',
                                'hashcode': hashcode}
                message_list.append(message_dict)
            hashcode_new = prompt(views.choose_message(message_list))['value']
            print(c.get_message(hashcode_new)['Message'])
            c.storage_manager.update_message_state(hashcode_new, 'RECEIVED')
        else:
            print('No messages')
    if op == 'View Spamers':
        spammers = c.get_spammers(10)
        for spammer in spammers:
            print(spammer[0] + ': {} '.format(int(spammer[1])) + 'spam messages')
    if op == 'View Online':
        online = c.get_online()
        print(online)
    if op == 'Quit':
        c.logoff()
        quit()
