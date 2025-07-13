# src/bot_helper/all.py

from src.address_book.core.address_book import AddressBook


def all(book: AddressBook):
    if not book.data:
        return "Address book is empty."

    output_lines = []
    for record in book.data.values():
        output_lines.append(str(record))

    return "\n".join(output_lines)
