# src/bot_helper/change_contact.py


from main import input_error, aliases
from src.address_book.core.address_book import AddressBook

@input_error
@aliases("change")
def change_contact(name: str, old_phone_number, new_phone_number: str, book: AddressBook):
    record = book.find(name)

    if record is None:
        raise KeyError("You're trying to change non existing contact, please add one before changing it.")

    return record.edit_phone(old_phone_number, new_phone_number)
