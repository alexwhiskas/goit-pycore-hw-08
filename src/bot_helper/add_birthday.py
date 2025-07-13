# src/bot_helper/add_birthday.py

from main import input_error

from src.address_book.core.address_book import AddressBook
from src.address_book.core.fields import Birthday


@input_error
def add_birthday(name: str, birthday: str, book: AddressBook) -> str:
    record = book.find(name)

    if not record:
        return f"No contact found with name '{name}'."

    record.birthday = Birthday(birthday)
    return f"Birthday set for {name}: {birthday}"
