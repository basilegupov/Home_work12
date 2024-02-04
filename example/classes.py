from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("Invalid value")

    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.is_valid(value):
            self.__value = new_value
        else:
            raise ValueError("Invalid value")


class Name(Field):
    pass


class Phone(Field):

    def is_valid(self, value):
        return value.isdigit() and len(value) == 10



class Birthday(Field):


    def is_valid(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        ph = Phone(phone)
        self.phones.append(ph)
        return ph

    def remove_phone(self, phone):
        phones = [p for p in self.phones if p.value != phone]
        if len(phones) == len(self.phones):
            raise ValueError("Phone not found")
        self.phones = phones

    def edit_phone(self, phone_old: str, phone_new: str):
        self.remove_phone(phone_old)
        self.add_phone(phone_new)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday_year = today.year
            birthday_this_year = datetime.strptime(self.birthday.value, '%Y-%m-%d').date().replace(year=next_birthday_year)
            if today > birthday_this_year:
                next_birthday_year += 1
                birthday_this_year = birthday_this_year.replace(year=next_birthday_year)
            days_left = (birthday_this_year - today).days
            return days_left
        else:
            return None

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        try:
            del self.data[name]
        except KeyError:
            pass

    def iterator(self, batch_size=10):
        records = list(self.data.values())
        num_records = len(records)
        current_idx = 0
        while current_idx < num_records:
            batch = records[current_idx:current_idx + batch_size]
            yield batch
            current_idx += batch_size

    def __str__(self):
        return '\n'.join(str(r) for r in self.data.values())