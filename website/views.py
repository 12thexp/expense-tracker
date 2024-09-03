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

    pd.set_option("display.float_format", "${:,.2f}".format)

    years_extraction = db.session.execute(
        db.session.query(extract("year", Transactions.date).label("year")).distinct()
    ).fetchall()
    years = [
        y[0] for y in years_extraction
    ]  # query execution extracts a tuple (year,), this cleans it to 'year'. type int

    year_selected = request.form.get("yearSelect")  # OSS it's of type string!!

    print("yearSelected:", type(year_selected))
    print("years[0]", type(years[0]))

    # create connector
    # engine = create_engine("sqlite:///instance/database.db")
    if year_selected is None:
        year_selected = datetime.today().year

    # create query object
    query = (
        db.session.query(Transactions.date, Transactions.category, Transactions.amount)
        .filter_by(flag="out")
        .filter(extract("year", Transactions.date).label("year") == year_selected)
    )

    df = pd.DataFrame(db.session.execute(query).fetchall())

    # db.session.query(
    #     Transactions.date, Transactions.category, Transactions.amount
    # ).filintter_by(flag="out"))

    # pass query string and connector to read_sql()
    # df = pd.read_sql(
    #     str(query.statement.compile(compile_kwargs={"literal_binds": True})), engine
    # )

    # print(df)

    df.date = pd.to_datetime(df.date).dt.strftime("%Y-%m")

    # create pivot table
    df_pivot = df.pivot_table(
        values="amount",
        index="category",
        columns="date",
        aggfunc=np.sum,
        margins=True,
        margins_name="Totals",
    )

    return render_template(
        "pivot-table.html",
        data=df_pivot.to_html(classes="table"),
        years=years,
        year_selected=int(year_selected),
    )
