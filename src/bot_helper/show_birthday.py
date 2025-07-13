# src/bot_helper/show_birthday.py

from main import input_error

from src.address_book.core.address_book import AddressBook


@input_error
def show_birthday(name: str, book: AddressBook) -> str:
    record = book.find(name)

    if record is None:
        return f"No contact found with name '{name}'."

    if not record.birthday:
        return f"No birthday set for {name}."

    return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
