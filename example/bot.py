import pickle
from classes import AddressBook, Record


class Bot:
    def __init__(self):
        self.file = 'contacts.txt'
        self.book = AddressBook()
        try:
            with open(self.file, 'rb') as f:
                contacts_dict = pickle.load(f)
                self.book.data = contacts_dict
        except:
            print('Created a new Adrressbook')

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
    def add_phone(self, name: str, number: str):
        'add Vova 1231231231'
        if name not in self.book.data:
            record = Record(name)
            self.book.add_record(record)
        else:
            record = self.book.find(name)
        record.add_phone(number)

    @input_error
    def change_phone(self, name: str, old_number: str, new_number: str):
        if name not in self.book.data:
            raise ValueError("Contact not found")
        record = self.book.find(name)
        record.edit_phone(old_number, new_number)

    def search(self, text):
        result = set()
        for record in self.book.data.values():
            if text in record.name.value:
                result.add(record)
            for phone in record.phones:
                if text in phone.value:
                    result.add(record)
        return '\n'.join([str(record) for record in result])

    # if text in record.name.value + ' '.join([p.value for p in record.phones])

    @input_error
    def show_phone(self, name: str):
        return self.book.find(name)

    def show_all(self, *args):
        return self.book

    def bye(self, *args):
        with open(self.file, 'wb') as f:
            pickle.dump(self.book.data, f)
        return "Good bye!"

    COMMANDS = {
        'hello': hello,
        'add': add_phone,
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
        if command in ['hello', 'exit', 'close']:
            pass
        elif command == 'add':
            if len(parameter) != 2:
                raise ValueError(f'Invalid parameters. Try again. Use "{command} <contact name> <phone number>"')
        elif command == 'change':
            if len(parameter) != 3:
                raise ValueError(f'Invalid parameters. Try again. Use "{command} <contact name> <phone number>"')
        elif command in ['phone', 'search']:
            if not parameter:
                raise ValueError(f'Invalid parameter. Try again. Use "{command} <contact name>"')
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
                if command in ['exit', 'close', 'good']:
                    self.bye(*parameters)
                    break
            except Exception as e:
                print(e)
