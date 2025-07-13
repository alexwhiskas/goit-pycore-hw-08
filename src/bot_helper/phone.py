# src/bot_helper/phone.py

from src.address_book.core.address_book import AddressBook


def phone(name: str, book: AddressBook):
    record = book.find(name)

    if record is None:
        raise KeyError(f"Unfortunately there's no contact with Name: {name}, please add one before checking their number.")
    else:
        return f"Contact with name '{record.name}' has following phone number(s): " + ", ".join(p.value for p in record.phones)