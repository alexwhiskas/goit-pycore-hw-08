# src/address_book/utils/validators.py

from functools import wraps


def validate_phone(func):
    @wraps(func)
    def wrapper(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        return func(self, value)
    return wrapper
