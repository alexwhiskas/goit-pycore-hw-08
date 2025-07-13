# src/address_book/core/fields.py

from datetime import datetime

from src.address_book.utils.validators import validate_phone


class Field:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    @validate_phone
    def __init__(self, value: str) -> None:
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
