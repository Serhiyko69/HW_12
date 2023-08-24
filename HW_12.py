import pickle
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.validate(val)
        self.__value = val

    def validate(self, value):
        pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number")

class Birthday(Field):
    def get_date(self):
        return datetime.strptime(self.value, '%Y-%m-%d')

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Field(name)
        self.phone = Phone(phone) if phone else None
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday and self.birthday.value:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.get_date().month, self.birthday.get_date().day)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.records, f)

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            self.records = pickle.load(f)

    def search(self, query):
        results = []
        queried_lower = query.lower()  

        for record in self.records:
            if (
                    queried_lower in record.name.value.lower() or
                    (record.phone and queried_lower in record.phone.value.lower())
            ):
                results.append(record)
        return results


# Створення адресної книги
address_book = AddressBook()
record1 = Record("Ivan Ivanov", phone="0965996655", birthday="1990-05-15")
record2 = Record("Olena Teliga", phone="0956543210")
address_book.add_record(record1)
address_book.add_record(record2)

# Збереження адресної книги на диск
address_book.save_to_file('address_book.pickle')

# Відновлення адресної книги з диска
restored_address_book = AddressBook()
restored_address_book.load_from_file('address_book.pickle')

# Пошук контактів за ім'ям або номером телефону
query = input("Enter search query: ")
search_results = restored_address_book.search(query)
for record in search_results:
    print(record.name.value)
    if record.phone:
        print("Phone:", record.phone.value)
    if record.birthday:
        print("Days to birthday:", record.days_to_birthday())
    print()

# Відкриваємо файл для читання у бінарному режимі
with open('address_book.pickle', 'rb') as f:
    restored_records = pickle.load(f)

# Створюємо об'єкт AddressBook з відновленими записами
restored_address_book = AddressBook()
restored_address_book.records = restored_records

# Виводимо інформацію про записи
for record in restored_address_book.records:
    print(record.name.value)
    if record.phone:
        print("Phone:", record.phone.value)
    if record.birthday:
        print("Days to birthday:", record.days_to_birthday())
    print()

