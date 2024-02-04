
phonebook = {}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    return wrapper


def hello(*args):
    return "How can I help you?"


@input_error
def add_phone(name: str, number: str):
    if name in phonebook:
        raise ValueError(f'Contact {name} already exist.')
    else:
        phonebook[name] = number
        return f'Contact {name} with phone {number} added.'


@input_error
def change_phone(name: str, number: str):
    if name in phonebook:
        phonebook[name] = number
        return f'Phone number of contact {name} changed to {number}.'
    else:
        raise IndexError("Contact not found")


@input_error
def show_phone(name: str):
    if name in phonebook:
        return f'{name}: {phonebook[name]}'
    else:
        raise IndexError("Contact not found")


def show_all(*args):
    if not phonebook:
        return 'Phonebook is empty.'
    phonebook_str = '|{:^16}|{:^16}|'.format('Name', 'Phone number') + '\n'
    for name, number in phonebook.items():
        phonebook_str += '|{:<16}|{:>16}|'.format(name, number) + '\n'

    return phonebook_str


def bye(*args):
    return "Good bye!"


COMMANDS = {
    'hello': hello,
    'add': add_phone,
    'change': change_phone,
    'phone': show_phone,
    'show': show_all,
    'good': bye,
    'exit': bye,
    'close': bye
}


def get_command(command):
    return COMMANDS[command]


@input_error
def parsing_input(input_str):
    if not input_str:
        raise ValueError("Empty command. Please try again.")
    command, *parameter = input_str.split(' ')
    command = command.lower()
    if command in ['hello', 'exit', 'close']:
        pass
    elif command == 'add':
        if len(parameter) != 2:
            raise ValueError('Invalid parameters. Try again. Use "add <contact name> <phone number>"')
    elif command == 'change':
        if len(parameter) != 2:
            raise ValueError('Invalid parameters. Try again. Use "change <contact name> <phone number>"')
    elif command == 'phone':
        if not parameter:
            raise ValueError('Invalid parameter. Try again. Use "phone <contact name>"')
    elif command == 'show':
        if not parameter or not parameter[0] == 'all':
            raise ValueError('Invalid command. Try again. Use "show all"')
    elif command == 'good':
        if not parameter or not parameter[0] == 'by':
            raise ValueError('Invalid command. Try again. Use "good by"')
    else:
        raise ValueError("Invalid command. Please try again.")
    command_str = command + ' ' + ' '.join(parameter)
    return command_str


def main():
    while True:
        input_str = input('Enter command>>').strip()
        try:
            command_str = parsing_input(input_str)
            command, *parameters = command_str.split()
            print(get_command(command)(*parameters))
            if command in ['exit', 'close', 'good']:
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
