from sqlalchemy import ForeignKey
from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Transactions(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), ForeignKey("categories.category"))
    # category = db.Column(db.String(50))
    amount = db.Column(db.Double, nullable=False)
    description = db.Column(db.String(200))
    flag = db.Column(db.String(2), nullable=False)
    tags = db.relationship("Tags", secondary="tag_transaction", backref="transactions")


class Categories(db.Model):

    __tablename__ = "categories"

    category = db.Column(db.String(50), primary_key=True)


class Tags(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)

    def __repr__(self):
        return f"{self.tag}"


tag_transaction = db.Table(
    "tag_transaction",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
    db.Column("transaction_id", db.Integer, db.ForeignKey("transactions.id")),
)


def init_db():
    """initialize the database with default data and test elements"""
    # default_categories = ["work", "food", "house", "car", "public transport"]
    default_categories = [
        "work",
        "medical",
        "groceries",
        "plants & gardening",
        "vehicles",
        "food from The Outside",
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
    for x in default_categories:
        db.session.merge(Categories(category=x))

    # test initialization
    from datetime import datetime, date

    transactions1 = Transactions(
        date=date.today(), category="house", amount=-98, flag="out"
    )
    transactions2 = Transactions(
        date=date.today(), category="plants & gardening", amount=-12, flag="out"
    )
    transactions3 = Transactions(
        date=date.today(), category="vehicles", amount=-80, flag="out"
    )
    transactions4 = Transactions(
        date=date.today(), category="food from The Outside", amount=-50, flag="out"
    )
    transactions5 = Transactions(
        date=date.today(), category="food from The Outside", amount=-20, flag="out"
    )
    transactions6 = Transactions(
        date=date.today(), category="work", amount=1000, flag="in"
    )

    tag1 = Tags(tag="motorbike")
    tag2 = Tags(tag="tech")
    tag3 = Tags(tag="wifi")
    tag4 = Tags(tag="fuel")
    tag5 = Tags(tag="sushi")
    tag6 = Tags(tag="lunch")
    tag7 = Tags(tag="social events")
    tag8 = Tags(tag="chinese")
    tag9 = Tags(tag="accenture")

    transactions1.tags.append(tag3)  # Tag the first Transactions with 'animals'
    transactions3.tags.append(tag1)  # Tag the third Transactions with 'cooking'
    transactions3.tags.append(tag4)  # Tag the third Transactions with 'tech'
    transactions4.tags.append(tag5)
    transactions4.tags.append(tag6)
    transactions4.tags.append(tag7)
    transactions5.tags.append(tag6)
    transactions5.tags.append(tag8)
    transactions6.tags.append(tag9)

    db.session.add_all(
        [
            transactions1,
            transactions2,
            transactions3,
            transactions4,
            transactions5,
            transactions6,
        ]
    )
    db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8])

    import csv

    with open(
        "/home/jarvis/Documents/python/expense-tracker/expenses_csv.csv", newline=""
    ) as f:
        t_list = csv.reader(f, delimiter=",")
        for t in t_list:
            print(t)
            tags = t[4].split(",")
            if t[5] == "out":
                t[2] = "-" + t[2]
            new_t = Transactions(
                date=datetime.strptime(t[0], "%Y-%m-%d"),
                category=t[1],
                amount=float(t[2]),
                description=t[3],
                flag=t[5],
            )
            for tag in tags:
                new_t.tags.append(Tags(tag=tag))

            db.session.add(new_t)
            db.session.add_all(new_t.tags)

    db.session.commit()
