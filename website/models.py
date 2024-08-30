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
    tags = db.relationship("Tags", secondary="transaction_tag", backref="transactions")


class Categories(db.Model):

    __tablename__ = "categories"

    category = db.Column(db.String(50), primary_key=True)


class Tags(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)

    def __repr__(self):
        return f'<Tag "{self.tag}">'


transaction_tag = db.Table(
    "transaction_tag",
    db.Column("transaction_id", db.Integer, db.ForeignKey("transactions.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
)


def init_db():
    """initialize the database with default data and test elements"""
    default_categories = ["work", "food", "house", "car", "public transport"]
    for x in default_categories:
        db.session.merge(Categories(category=x))

    # test initialization
    from datetime import datetime, date

    transactions1 = Transactions(
        date=date.today(), category="house", amount=98, flag="out"
    )
    transactions2 = Transactions(
        date=date.today(), category="plants", amount=12, flag="out"
    )
    transactions3 = Transactions(
        date=date.today(), category="car", amount=80, flag="out"
    )

    tag1 = Tags(tag="vehicles")
    tag2 = Tags(tag="tech")
    tag3 = Tags(tag="wifi")
    tag4 = Tags(tag="fuel")

    transactions1.tags.append(tag3)  # Tag the first Transactions with 'animals'
    transactions3.tags.append(tag1)  # Tag the third Transactions with 'cooking'
    transactions3.tags.append(tag4)  # Tag the third Transactions with 'tech'
    transactions3.tags.append(tag4)  # Tag the third Transactions with 'writing'

    db.session.add_all([transactions1, transactions2, transactions3])
    db.session.add_all([tag1, tag2, tag3, tag4])

    db.session.commit()
