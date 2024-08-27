from flask import Blueprint, render_template, request, redirect, session, flash, json, jsonify
from sqlalchemy import text
from .models import Transactions, Categories
from . import db
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():

    history = Transactions.query.order_by(Transactions.id.desc()).all()
    categories = Categories.query.order_by(Categories.category.asc()).all()
    
    if request.method == 'POST':
        flag = request.form.get('flag')
        date = request.form.get('date')
        tdate = datetime.strptime(date, '%Y-%m-%d').date()
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        if flag == 'out':
            amount = -amount
        description = request.form.get('description')

        new_transaction = Transactions(date=tdate, category=category, amount=amount, description=description, flag=flag)

        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction inserted!', category='success')

        db.session.merge(Categories(category=category))
        categories = Categories.query.order_by(Categories.category.asc()).all()
        history = Transactions.query.order_by(Transactions.date.desc()).all()

        return render_template("home.html", history=history, categories=categories)
    
    return render_template("home.html", history=history)

@views.route('/stats')
def stats():
    return render_template("stats.html")

@views.route('/income')
def income():
    return render_template("income.html")

@views.route('/expenses')
def expenses():
    return render_template("expenses.html")


@views.route('/delete-row', methods=['POST'])
def delete_row():
    row = json.loads(request.data)
    rowId = row['rowId']
    row = Transactions.query.get(rowId)
    
    if row:
        db.session.delete(row)
        db.session.commit()

    flash('row deleted...', category='success')

    history = Transactions.query.order_by(Transactions.id.desc()).all()

    return jsonify({})

@views.route('/edit')
def edit():
    history = Transactions.query.order_by(Transactions.id.desc()).all()
    return render_template("edit.html", history=history)