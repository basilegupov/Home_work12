from collections import UserDict
from datetime import datetime  # timedelta


class Field:
    def __init__(self, value=None):
        if not self.is_valid(value):
            print('????')
            raise ValueError
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError
        self.__value = new_value

    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.value)


class Name(Field):

    def is_valid(self, value):
        return isinstance(value, str)


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone number format.")
        super().__init__(value)

    def is_valid(self, value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value=None):
        if not self.is_valid(value):
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")
        datetime.strptime(new_value, "%Y-%m-%d")
        self.__value = new_value

    def is_valid(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False
        else:
            return True


class Record:
    def __init__(self, name_contact, birthday=None):
        self.name = Name(name_contact)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else birthday

    def add_phone(self, phone):
        phone_field = Phone(phone)
        self.phones.append(phone_field)

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        phones = [p for p in self.phones if p.value != phone]
        if len(phones) == len(self.phones):
            raise ValueError('Phone not found')
        self.phones = phones

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError(f"Phone number {old_phone} not exist in {self.phones}.")

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()
        next_birthday = datetime(today.year, birthday.month, birthday.day).date()
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()
        return (next_birthday - today).days

    def __str__(self):
        # return (f"Contact name: {str(self.name.value)}, "
        #         f"phones: {'; '.join(str(p.value) for p in self.phones)}")
        if self.birthday:
            return (f"Contact name: {str(self.name.value)}, birthday: {str(self.birthday.value)},"
                    f" phones: {'; '.join(str(p.value) for p in self.phones)}")
        else:
            return (f"Contact name: {str(self.name.value)}, "
                    f" phones: {'; '.join(str(p.value) for p in self.phones)}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name_contact):
        return self.data.get(name_contact, None)

    def delete(self, name_contact):
        if name_contact in self.data:
            del self.data[name_contact]

    def iterator(self, page_size=10):
        total_records = len(self.data)
        ind = 0
        while ind < total_records:
            yield list(self.data.values())[ind:ind + page_size]
            ind += page_size

    def __str__(self):
        return '\n'.join(str(r) for r in self.data.values())
