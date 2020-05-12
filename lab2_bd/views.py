operations_user = [
    {
        'type': 'list',
        'message': 'Select operation',
        'name': 'operation',
        'choices': [
            {
                'name': 'Create message'
            },
            {
                'name': 'View Inbox'
            },
            {
                'name': 'Quit'
            }
        ]
    }
]

operations_admin = [
    {
        'type': 'list',
        'message': 'Select operation',
        'name': 'operation',
        'choices': [
            {
                'name': 'Create message'
            },
            {
                'name': 'View Inbox'
            },
            {
                'name': 'View Spamers'
            },
            {
                'name': 'View Online'
            },
            {
                'name': 'Quit'
            }
        ]
    }
]

input_name = [{
    'type': 'input',
    'name': 'value',
    'message': 'Enter the name'
}]

input_message = [{
    'type': 'input',
    'name': 'value',
    'message': 'Enter the message'
}]

input_receiver = [{
    'type': 'input',
    'name': 'value',
    'message': 'Enter the Receiver'
}]

choice_register = [{
    'type': 'list',
    'name': 'value',
    'message': 'Do you want to register',
    'choices': [
            {
                'name': 'Yes'
            },
            {
                'name': 'No'
            }
        ]
}]


def choose_message(messages):
    choice_message = [
        {
            'type': 'list',
            'name': 'value',
            'message': 'Choose message to view',
            'choices': []
        }
    ]
    for message in messages:
        obj = {
            'value': message['hashcode'],
            'name': message['message_str']
        }
        choice_message[0]['choices'].append(obj)
    return choice_message
