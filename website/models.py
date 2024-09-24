from sqlalchemy import ForeignKey
from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime, date
import csv


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
    for x in default_categories:
        db.session.merge(Categories(category=x))

    # test initialization
    load_csv("aly_exp.csv")
    load_csv("test_expenses.csv")







def load_csv(filename: str):
    with open(filename, newline="") as f:
        t_list = csv.reader(f, delimiter=",")
        for t in t_list:
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
