from collections import UserDict
from datetime import datetime  # timedelta


class Field:
    def __init__(self, value=None):
        if not self.is_valid(value):
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
        pass

    def __str__(self):
        return str(self.value)


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError
        self.__value = new_value

    def is_valid(self, value):
        return isinstance(value, str)


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone number format.")
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid phone number format.")
        self.__value = new_value

    def is_valid(self, value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Birthday(Field):
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
        if not value:
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False

        return True


class Record:
    def __init__(self, name_contact, birthday=None):
        self.name = Name(name_contact)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else birthday

    def add_phone(self, phone):
        phone_field = Phone(phone)
        self.phones.append(phone_field)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

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
        # print(type(self.birthday.value))
        birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()

        next_birthday = datetime(today.year, birthday.month, birthday.day).date()
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()
        return (next_birthday - today).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


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


if __name__ == "__main__":
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John", birthday="1995-01-01")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення запису для Mike
    mike_record = Record("Mike", birthday="1995-03-01")
    mike_record.add_phone("1234545321")
    mike_record.add_phone("4444444444")

    # Додавання запису Mike до адресної книги
    book.add_record(mike_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Створення та додавання нового запису для Jimmy
    jimmy_record = Record("Jimmy")
    jimmy_record.add_phone("7776543210")
    book.add_record(jimmy_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    result = book.find("John")
    if result:
        print(result.name.value, [phone.value for phone in result.phones])
        print(f"Days to next birthday: {result.days_to_birthday()}")

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    found_phone = john.find_phone("5555555554")
    print(f"{john.name}: {found_phone}")  # Виведення: None

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Посторінковий вивід
    numb_page = 1
    for batch in book.iterator(page_size=1):
        print(f'page {numb_page}')
        for record in batch:
            print(record)

        numb_page += 1

    # Видалення запису Jane
    book.delete("Jane")
