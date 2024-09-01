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
from sqlalchemy import text
from .models import Transactions, Categories, Tags, tag_transaction
from . import db
from datetime import datetime


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():

    history = Transactions.query.order_by(Transactions.id.desc()).all()
    categories = Categories.query.order_by(Categories.category.asc()).all()

    if request.method == "POST":
        date: str = request.form.get("date")
        tdate: datetime = datetime.strptime(date, "%Y-%m-%d").date()
        amount: float = float(request.form.get("amount"))
        category: str = request.form.get("category")
        description: str = request.form.get("description")
        tags: list[str] = request.form.get("tags-input").split(",")
        flag: str = request.form.get("flag")

        if flag == "out":
            amount = -amount

        new_transaction = Transactions(
            date=tdate,
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

        categories = Categories.query.order_by(Categories.category.asc()).all()
        history = Transactions.query.order_by(Transactions.date.desc()).all()

        return render_template("home.html", history=history, categories=categories)

    return render_template("home.html", history=history, categories=categories)


def tags_to_db(tags: list, transaction: Transactions) -> None:
    """create Tags object from each tag in the list and insert into db"""
    for t in tags:
        t_obj = Tags(tag=t)
        db.session.add(t_obj)
        transaction.tags.append(t_obj)  # tag the transactions with tag t


@views.route("/stats")
def stats():
    return render_template("stats.html")


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
