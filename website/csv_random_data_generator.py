from faker import Faker
from wonderwords import RandomWord
import random
import csv


fake = Faker()

default_categories = [
    "work",
    "medical",
    "groceries",
    "plants & gardening",
    "vehicles",
    "food",
    "public transport",
    "phone",
    "entertainment",
    "things",
    "house",
    "haircuts",
    "travel",
    "art",
    "gifts",
    "other",
]

flag = ["in", "out"]


generate = False

if generate:
    # generate rows of random transaction data and write to csv
    with open("test_expenses.csv", "w") as f:
        for i in range(0, 1000):
            row = ""
            date = str(fake.date_between(start_date="-5y", end_date="today")) + ","
            cat = random.choice(default_categories) + ","
            amount = str(random.randint(100, 50000) / 100) + ","

            desc = ""
            for j in range(1, 6):
                desc += RandomWord().word()
                if j < 5:
                    desc += " "
            desc += ","

            tags = ""
            for z in range(1, 4):
                tags += RandomWord().word()
                if z < 3:
                    tags += ","
            tags = '"' + tags + '"' + ","

            fl = '"' + random.choice(flag) + '"'

            row = date + cat + amount + desc + tags + fl

            f.write(row + "\n")
