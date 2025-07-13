# src/address_book/core/address_book.py

from typing import Optional
from collections import UserDict
from datetime import datetime, timedelta

from .record import Record


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today_date = datetime.today().date()
        upcoming_birthdays = []

        # processing users birthdays
        for record in self.data.values():
            name         = record.name
            birthday_date = record.birthday

            if record.birthday is None:
                continue

            # replacing birthday year with current year
            birthday_this_year = birthday_date.value.replace(year=today_date.year)

            # handling cases for January birthdays
            if birthday_this_year < today_date:
                birthday_this_year = birthday_this_year.replace(year=birthday_this_year.year + 1)

            # checking current week birthdays
            if 0 <= (birthday_this_year - today_date).days < 7:
                congratulation_date = birthday_this_year

                # if birthday will be on the weekend - moving congratulation date to next monday
                if congratulation_date.weekday() in (5, 6):
                    days_to_monday       = 7 - congratulation_date.weekday()
                    congratulation_date += timedelta(days=days_to_monday)

                upcoming_birthdays.append({
                    "name": name,
                    "congratulation_date": congratulation_date
                })

        return [
            f"{b['name']} — {b['congratulation_date'].strftime("%A, %d.%m.%Y")}"
            for b in sorted(upcoming_birthdays, key=lambda x: x["congratulation_date"])
        ]