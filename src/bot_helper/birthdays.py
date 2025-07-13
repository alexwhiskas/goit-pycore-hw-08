# src/bot_helper/birthdays.py

from main import input_error

from src.address_book.core.address_book import AddressBook


@input_error
def birthdays(book: AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + "\n".join(upcoming_birthdays)
    else:
        return "No birthdays in the next 7 days."
