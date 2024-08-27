from sqlalchemy import ForeignKey
from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
    

class Transactions(db.Model):

    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # category = db.Column(db.String(50), ForeignKey('categories.category'))
    category = db.Column(db.String(50))
    amount = db.Column(db.Double, nullable=False)
    description = db.Column(db.String(200))
    flag = db.Column(db.String(2), nullable=False)


class Categories(db.Model):

    __tablename__ = 'categories'

    # id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), primary_key=True)
    # establish the one-to-many relation here
    # transaction = db.relationship('Transactions', backref='Categories', lazy='dynamic')



def init_db():

    db.create_all()
