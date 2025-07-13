# src/address_book/core/record.py

from typing import Optional
from .fields import Name, Phone, Birthday


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = birthday

    def add_phone(self, phone_number: str) -> None:
        phone = Phone(phone_number)
        self.phones.append(phone)

    def edit_phone(self, old_number: str, new_number: str) -> str:
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)

                return f"Updated contact for {self.name}, replaced old phone number {old_number} with new phone number: {new_number}"

        raise ValueError("Phone number not found.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def remove_phone(self, phone_number: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone_number]

    def __str__(self) -> str:
        birthday_part = ""
        birthday_value = self.birthday

        if birthday_value is not None:
            birthday_part = f", birthday: {self.birthday.value}"

        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_part}"
