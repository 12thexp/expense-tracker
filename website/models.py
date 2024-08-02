from . import db
from sqlalchemy.sql import func
    

class Transactions(db.Model):
    # timestamp = db.Column(db.DateTime(timezone=True), default=func.now)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    category = db.Column(db.String(50))
    amount = db.Column(db.Double)
    description = db.Column(db.String(200))
    flag = db.Column(db.String(2))
