import calendar
import sqlite3
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    json,
    jsonify,
    url_for,
)
from sqlalchemy import create_engine, extract, text, func
from sqlalchemy.sql import extract
from .models import Transactions, Categories, Tags, tag_transaction
from . import db
from datetime import datetime
import pandas as pd
import numpy as np
from io import StringIO


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():

    set_values()

    if request.method == "POST":
        flag: str = request.form.get("flag")

        date: datetime = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()

        amount: float = float(request.form.get("amount"))
        amount = set_expense(amount, flag)

        category: str = request.form.get("category")
        description: str = request.form.get("description")
        tags: list[str] = request.form.get("tags-input").split(",")

        new_transaction = Transactions(
            date=date,
            category=category,
            amount=amount,
            description=description,
            flag=flag,
        )

        db.session.add(new_transaction)
        tags_to_db(tags, new_transaction)
        db.session.merge(Categories(category=category))
        db.session.commit()
        flash("transaction inserted!", category="success")

        set_values()

        return render_template(
            "home.html",
            history=history,
            categories=categories,
            totIncome="{0:.2f}".format(income.total),
            totExpense="{0:.2f}".format(expenses.total),
            balance="{0:.2f}".format(balance),
        )

    return render_template(
        "home.html",
        history=history,
        categories=categories,
        totIncome="{0:.2f}".format(income.total),
        totExpense="{0:.2f}".format(expenses.total),
        balance="{0:.2f}".format(balance),
    )


def set_values():
    global categories
    global history
    global expenses
    global income
    global balance

    categories = Categories.query.order_by(Categories.category.asc()).all()
    history = Transactions.query.order_by(Transactions.date.desc()).all()

    expenses = (
        Transactions.query.with_entities(func.sum(Transactions.amount).label("total"))
        .filter_by(flag="out")
        .first()
    )

    income = (
        Transactions.query.with_entities(func.sum(Transactions.amount).label("total"))
        .filter_by(flag="in")
        .first()
    )

    balance = income.total + expenses.total


def set_expense(amount, flag):
    if flag == "out":
        amount = -amount
    return amount


def tags_to_db(tags: list, transaction: Transactions) -> None:
    """create Tags object from each tag in the list and insert into db"""
    for t in tags:
        t_obj = Tags(tag=t)
        db.session.add(t_obj)
        transaction.tags.append(t_obj)  # tag the transactions with tag t


@views.route("/analytics")
def analytics():
    return render_template("analytics.html")


@views.route("/income")
def income():
    return render_template("income.html")


@views.route("/expenses")
def expenses():
    return render_template("expenses.html")


@views.route("/delete-row", methods=["POST"])
def delete_row():
    row = json.loads(request.data)
    rowId = row["rowId"]
    row = Transactions.query.get(rowId)

    if row:
        db.session.delete(row)
        db.session.commit()

    flash("going going gone...", category="success")

    return jsonify({})


@views.route("/edit")
def edit():
    history = Transactions.query.order_by(Transactions.id.desc()).all()
    return render_template("edit.html", history=history)


@views.route("/filter-tag", methods=["GET", "POST"])
def filter_tag():
    t = json.loads(request.data)["tag"]
    return url_for("views.filter_tag_t", tag=t)


@views.route("/filter-tag/<tag>", methods=["GET"])
def filter_tag_t(tag):
    filtered = Transactions.query.join(tag_transaction).join(Tags).filter_by(tag=tag)
    return render_template("filter-tag.html", filtered=filtered, tag=tag)


@views.route("/pivot-table", methods=["GET", "POST"])
def pivot_table():

    pd.set_option("display.float_format", "{:.2f}".format)

    # distinct years for which we have trasnactions -> for the filtering select dropdown
    years = extract_years()
    print(years)

    year_selected = request.form.get("year-select")  # OSS it's of type string!!
    print(year_selected)

    if year_selected is None:
        year_selected = datetime.today().year

    exp_pivot = pivot_calc(flag="out", year_selected=year_selected)
    exp_pivot.fillna(0, inplace=True)

    inc_pivot = pivot_calc(flag="in", year_selected=year_selected)
    inc_pivot.fillna(0, inplace=True)

    balance_pivot = exp_pivot.add(inc_pivot, fill_value=0)

    balance_html = style_balance_pivot(balance_pivot)

    return render_template(
        "pivot-table.html",
        exp_pivot=exp_pivot.replace(0, "-").to_html(classes="table"),
        inc_pivot=inc_pivot.replace(0, "-").to_html(classes="table"),
        balance_pivot=balance_html,
        years=years,
        year_selected=int(year_selected),
    )


def extract_years():
    # extract distinct years of past transactions
    years_extraction = db.session.execute(
        db.session.query(extract("year", Transactions.date).label("year")).distinct()
    ).fetchall()
    years = [
        y[0] for y in years_extraction
    ]  # query execution extracts a tuple (year,), this cleans it to 'year'. type int

    years.sort(reverse=True)

    return years


def pivot_calc(flag, year_selected):
    # create query object for Transactions of selected year
    query = (
        db.session.query(Transactions.date, Transactions.category, Transactions.amount)
        .filter_by(flag=flag)
        .filter(extract("year", Transactions.date).label("year") == year_selected)
    )

    df = pd.DataFrame(db.session.execute(query).fetchall())

    df.date = pd.to_datetime(df.date).dt.strftime("%m")

    # create pivot table
    df_pivot = df.pivot_table(
        values="amount",
        index="category",
        columns="date",
        aggfunc=np.sum,
        margins=True,
        margins_name="Totals",
    )

    return df_pivot


def style_balance_pivot(balance_pivot):
    # to style format table with red/green amounts... sigh. save the html code then find and replace relevant bits to
    # use same class as homepage style amounts
    buff = StringIO()
    balance_pivot.replace(0, "-").to_html(buff)
    balance_html = buff.getvalue()

    replacements = [
        ('class="dataframe">', 'class="table">'),
        ("<td>", '<td><div class="amount-flag">'),
        ("</td>", "</div></td>"),
    ]
    for k, v in replacements:
        balance_html = balance_html.replace(k, v)

    return balance_html
