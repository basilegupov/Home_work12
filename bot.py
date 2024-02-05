import pickle
from classes import AddressBook, Record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e

    return wrapper


class Bot:
    def __init__(self):
        self.file = 'contacts.txt'
        self.book = AddressBook()
        try:
            with open(self.file, 'rb') as f:
                contacts_dict = pickle.load(f)
                self.book.data = contacts_dict
        except FileNotFoundError:
            print('Created a new Addressbook')

    @input_error
    def hello(*args):
        return ("How can I help you?\n"
                "Usage: command [*parameters]\n"
                "Commands:\n"
                "add <name> <phone> - add new contact and phone number\n"
                "rename <old_name> <new_name> - rename contact\n"
                "birthday <name> <birthday> - set up birthday (YYYY-mm-dd) of contact\n"
                "when <name> - how many days to next birthday of contact\n"
                "change <name> <old phone> <new phone> - change phone number of contact\n"
                "phone <name> - show all phones of contact\n"
                "show all  - show all contacts in the addressbook\n"
                "search <text> - search and show contacts containing any text"
                "good by | exit | close - close the bot\n"
                "hello | help - this message")

    @input_error
    def add_phone(self, name: str, number: str):
        if name not in self.book.data:
            record = Record(name)
            self.book.add_record(record)
        else:
            record = self.book.find(name)
        record.add_phone(number)
        return 'Ok'

    @input_error
    def set_birthday(self, name: str, birthday: str):
        record = self.book.find(name)
        if record:
            record.set_birthday(birthday)
        else:
            raise ValueError(f"Contact {name} not found")
        return 'Ok'

    @input_error
    def rename_contact(self, old_name: str, new_name: str):
        return self.book.rename_contact(old_name, new_name)

    @input_error
    def days_to_birthday(self, name: str):
        record = self.book.find(name)
        if record:
            days = record.days_to_birthday()
            if days:
                return days
            else:
                return f"Contact {name} has no birthday"
        else:
            raise ValueError(f"Contact {name} not found")

    @input_error
    def change_phone(self, name: str, old_number: str, new_number: str):
        if name not in self.book.data:
            raise ValueError(f"Contact {name} not found")
        record = self.book.find(name)
        record.edit_phone(old_number, new_number)

    @input_error
    def search(self, text: str):
        result = set()
        for record in self.book.data.values():
            if text in record.name.value:
                result.add(record)
            for phone in record.phones:
                if text in phone.value:
                    result.add(record)
        return '\n'.join([str(record) for record in result]) if result else f'{text} is not found in addressbook'

    # if text in record.name.value + ' '.join([p.value for p in record.phones])

    @input_error
    def show_phone(self, name: str):
        return self.book.find(name)

    @input_error
    def show_all(self, *args):
        return self.book

    @input_error
    def bye(self, *args):
        with open(self.file, 'wb') as f:
            pickle.dump(self.book.data, f)
        return "Good bye!"

    COMMANDS = {
        'hello': hello,
        'help': hello,
        'add': add_phone,
        'rename': rename_contact,
        'birthday': set_birthday,
        'when': days_to_birthday,
        'change': change_phone,
        'phone': show_phone,
        'show': show_all,
        'search': search,
        'good': bye,
        'exit': bye,
        'close': bye
    }

    def get_command(self, command):
        return self.COMMANDS[command]

    @input_error
    def parsing_input(self, input_str):
        if not input_str:
            raise ValueError("Empty command. Please try again.")
        command, *parameter = input_str.split(' ')
        command = command.lower()
        if command in ['hello', 'exit', 'close', 'help']:
            pass
        elif command == 'add':
            if len(parameter) != 2:
                raise ValueError(f'Invalid parameters. Try again. Use "{command} <contact name> <phone number>"')
        elif command == 'birthday':
            if len(parameter) != 2:
                raise ValueError(f'Invalid parameters. Try again. Use "{command} <contact name> <birthday>"')
        elif command == 'rename':
            if len(parameter) != 2:
                raise ValueError(f'Invalid parameters. Try again. Use "{command} <contact name> <new name>"')
        elif command == 'change':
            if len(parameter) != 3:
                raise ValueError(f'Invalid parameters. Try again. Use "{command} <contact name>  <old number> <new '
                                 f'number>"')
        elif command in ['phone', 'when']:
            if not parameter:
                raise ValueError(f'Invalid parameter. Try again. Use "{command} <contact name>"')
        elif command == 'search':
            if not parameter:
                raise ValueError(f'Invalid parameter. Try again. Use "{command} <searching text>"')
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

    def run(self):
        while True:
            input_str = input('Enter command>>').strip()
            try:
                command_str = self.parsing_input(input_str)
                command, *parameters = command_str.split()
                print(self.get_command(command)(self, *parameters))
                with open(self.file, 'wb') as f:
                    pickle.dump(self.book.data, f)
                if command in ['exit', 'close', 'good']:
                    # self.bye(*parameters)
                    break
            except Exception as e:
                print(e)
