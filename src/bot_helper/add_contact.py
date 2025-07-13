# src/bot_helper/add_contact.py

from main import input_error, aliases

from src.address_book.core.address_book import AddressBook
from src.address_book.core.record import Record


@input_error
@aliases("add")
def add_contact(name: str, phone_number: str, book: AddressBook):
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone_number)
        book.add_record(record)
        message = f"Added new contact with name: {name}, phone number: {phone_number}"
    else:
        if record.find_phone(phone_number) is None:
            record.add_phone(phone_number)
            message = f"Added new phone number: {phone_number} to contact with name: {name}"
        else:
            message = f"Contact with name: {name} already has phone: {phone_number}"

    return message
