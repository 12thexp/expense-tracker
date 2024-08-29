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
    tag = db.relationship("Tags", secondary="transaction_tag", backref="transactions")


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
    default_categories = ["work", "food", "house", "car", "public transport"]
    for x in default_categories:
        db.session.merge(Categories(category=x))
    db.session.commit()
