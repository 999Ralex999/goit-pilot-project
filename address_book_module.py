from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Please enter a valid name")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone must be 10 digits")
        super().__init__(value)

    def validate(self, phone):
        return len(phone) == 10 and phone.isdigit()


class Email(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid email format")
        super().__init__(value)

    def validate(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Address(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        raise ValueError(f"Phone {old_phone} not found")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        email = self.email.value if self.email else "No email"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "No birthday"
        address = self.address.value if self.address else "No address"
        return f"Name: {self.name.value}, Phones: {phones}, Email: {email}, Birthday: {birthday}, Address: {address}"

    def __getstate__(self):
        return {
            'name': self.name.value,
            'phones': [p.value for p in self.phones],
            'email': self.email.value if self.email else None,
            'birthday': self.birthday.value.strftime("%d.%m.%Y") if self.birthday else None,
            'address': self.address.value if self.address else None
        }

    def __setstate__(self, state):
        self.name = Name(state['name'])
        self.phones = [Phone(p) for p in state['phones']]
        self.email = Email(state['email']) if state['email'] else None
        self.birthday = Birthday(state['birthday']) if state['birthday'] else None
        self.address = Address(state['address']) if state['address'] else None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        return self.data.pop(name, None)

    def search(self, keyword):
        results = []
        for record in self.data.values():
            if keyword.lower() in str(record).lower():
                results.append(record)
        return results

    def get_upcoming_birthdays(self, days_ahead=7):
        today = datetime.now()
        upcoming = []
        for user in self.data.values():
            user_birthday = self.__get_user_birthday(user)
            if user_birthday and self.__is_birthday_upcoming(user_birthday, days_ahead):
                upcoming.append(self.__get_user_notification(user, user_birthday))
        return upcoming

    def __get_user_birthday(self, user):
        if user.birthday is None:
            return None
        today = datetime.now()
        b_day = user.birthday.value.replace(year=today.year)
        if b_day < today:
            b_day = b_day.replace(year=today.year + 1)
        return b_day

    def __is_birthday_upcoming(self, birthday, days_ahead):
        today = datetime.now()
        delta = (birthday - today).days
        return 0 <= delta < days_ahead

    def __get_user_notification(self, user, birthday):
        notify_date = self.__get_notification_date(birthday)
        return {
            'name': user.name.value,
            'congratulation_date': notify_date.strftime('%Y.%m.%d')
        }

    def __get_notification_date(self, birthday):
        if birthday.weekday() == 5:
            birthday += timedelta(days=2)
        elif birthday.weekday() == 6:
            birthday += timedelta(days=1)
        return birthday

    def __getstate__(self):
        return dict(self.data)

    def __setstate__(self, state):
        self.data = state
