from cs50 import SQL
from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime


# Configure CS50 Library to use SQLite database
db = SQL("__link to postgres database (sensitive information)__")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """Escape special characters: https://github.com/jacebrowning/memegen#special-characters"""
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """Decorate routes to require login: http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def format_list(list):
    """Format list extracted from database for passing to html template"""
    for row in list:
        if not row["duedate"]:
            row["duedate"] = "-"
        if row["completedtime"]:
            completedtime = (row["completedtime"]).strftime("%Y-%m-%d %H:%M")
            row["completedtime"] = completedtime


def query_shopping_lists():
    """Query un-deleted shopping lists"""
    return db.execute("SELECT * FROM shopping WHERE userId = :user_id AND deleted is False "
                      "ORDER BY completed, duedate is NULL, duedate, transacted DESC",
                      user_id=session["user_id"])


def query_todo_lists():
    """Query un-deleted to-do lists"""
    return db.execute("SELECT * FROM todo WHERE userId = :user_id AND deleted is False "
                      "ORDER BY completed, duedate is NULL, duedate, transacted DESC",
                      user_id=session["user_id"])


def add_shopping_list(listname, duedate):
    """Insert new list into "shopping" table"""
    db.execute("INSERT INTO shopping (userid, listname, duedate, transacted)"
               "VALUES (:user_id, :listname, :duedate, :datetime)",
               user_id=session["user_id"], listname=listname, duedate=duedate, datetime=datetime.now())

def add_todo_list(listname, duedate):
    """Insert new list into "to-do" table"""
    db.execute("INSERT INTO todo (userid, listname, duedate, transacted)"
               "VALUES (:user_id, :listname, :duedate, :datetime)",
               user_id=session["user_id"], listname=listname, duedate=duedate, datetime=datetime.now())


def delete_shopping_list(shoppingid):
    """Update "shopping" table to reflect shopping list as deleted"""
    db.execute("UPDATE shopping SET deleted = True, transacted = :datetime WHERE shoppingid = :shoppingid",
               shoppingid=shoppingid, datetime=datetime.now())


def delete_todo_list(todoid):
    """Update "to-do" table to reflect to-do list as deleted"""
    db.execute("UPDATE todo SET deleted = True, transacted = :datetime WHERE todoid = :todoid",
               todoid=todoid, datetime=datetime.now())


def tick_shopping_list(shoppingid):
    """Update "shopping" table to reflect shopping list as completed"""
    db.execute("UPDATE shopping SET completed = True, transacted = :datetime, completedtime = :datetime WHERE shoppingid = :shoppingid",
               shoppingid=shoppingid, datetime=datetime.now())


def tick_todo_list(todoid):
    """Update "to-do" table to reflect to-do list as completed"""
    db.execute("UPDATE todo SET completed = True, transacted = :datetime, completedtime = :datetime WHERE todoid = :todoid",
               todoid=todoid, datetime=datetime.now())


def edit_shopping_list(shoppingid, listname, duedate):
    """Update shopping list details in "shopping" table"""
    db.execute("UPDATE shopping SET listname = :listname, duedate = :duedate WHERE shoppingid = :shoppingid",
               listname=listname, duedate=duedate, shoppingid=shoppingid)


def edit_todo_list(todoid, listname, duedate):
    """Update to-do list details in "to-do" table"""
    db.execute("UPDATE todo SET listname = :listname, duedate = :duedate WHERE todoid = :todoid",
               listname=listname, duedate=duedate, todoid=todoid)


def query_shopping_list_details(shoppingid):
    """Query shopping list details"""
    return db.execute("SELECT * FROM shopping WHERE userid = :user_id AND shoppingid = :shoppingid",
                      user_id=session["user_id"], shoppingid=shoppingid)[0]


def query_todo_list_details(todoid):
    """Query to-do list details"""
    return db.execute("SELECT * FROM todo WHERE userid = :user_id AND todoid = :todoid",
                      user_id=session["user_id"], todoid=todoid)[0]


def query_shopping_list(shoppingid):
    """Query un-deleted items in shopping list"""
    return db.execute("SELECT * FROM shopitem WHERE shoppingid = :shoppingid AND deleted is False ORDER BY completed, transacted DESC",
                      shoppingid=shoppingid)


def query_todo_list(todoid):
    """Query un-deleted items in to-do list"""
    list_1 = db.execute("SELECT * FROM todoitem WHERE todoid = :todoid AND deleted is False "
                        "ORDER BY completed, duedate is NULL, duedate, transacted DESC",
                        todoid=todoid)
    return list_1


def add_shopping_item(shoppingid, itemname):
    """Insert new list into "shopitem" table"""
    return db.execute("INSERT INTO shopitem (shoppingid, itemname, transacted) VALUES (:shoppingid, :itemname, :datetime)",
                      shoppingid=shoppingid, itemname=itemname, datetime=datetime.now())


def add_todo_item(todoid, itemname, duedate):
    """Insert new list into "todoitem" table"""
    return db.execute("INSERT INTO todoitem (todoid, itemname, duedate, transacted) VALUES (:todoid, :itemname, :duedate, :datetime)",
                      todoid=todoid, itemname=itemname, duedate=duedate, datetime=datetime.now())


def delete_shopping_item(itemid):
    """Update "shopitem" table to reflect item as deleted"""
    return db.execute("UPDATE shopitem SET deleted = True, transacted = :datetime WHERE itemid = :itemid",
                      itemid=itemid, datetime=datetime.now())


def delete_todo_item(itemid):
    """Update "todoitem" table to reflect item as deleted"""
    return db.execute("UPDATE todoitem SET deleted = True, transacted = :datetime WHERE itemid = :itemid",
                      itemid=itemid, datetime=datetime.now())


def tick_shopping_item(itemid):
    """Update "shopitem" table to reflect item as completed"""
    return db.execute("UPDATE shopitem SET completed = True, transacted = :datetime, completedtime = :datetime WHERE itemid = :itemid",
                      itemid=itemid, datetime=datetime.now())


def tick_todo_item(itemid):
    """Update "todoitem" table to reflect item as completed"""
    return db.execute("UPDATE todoitem SET completed = True, transacted = :datetime, completedtime = :datetime WHERE itemid = :itemid",
                      itemid=itemid, datetime=datetime.now())


def delete_shoppinglists(input):
    """Delete shopping lists based on input"""
    return db.execute("UPDATE shopping SET deleted = True, transacted = :datetime WHERE completed = :input AND userid = :user_id",
                      input=input, user_id=session["user_id"], datetime=datetime.now())


def delete_todolists(input):
    """Delete to-do lists based on input"""
    return db.execute("UPDATE todo SET deleted = True, transacted = :datetime WHERE completed = :input AND userid = :user_id",
                      input=input, user_id=session["user_id"], datetime=datetime.now())


def delete_shoppingitems(shoppingid, input):
    """Delete shopping items based on input"""
    return db.execute("UPDATE shopitem SET deleted = True, transacted = :datetime WHERE completed = :input AND shoppingid = :shoppingid",
                      input=input, shoppingid=shoppingid, datetime=datetime.now())


def delete_todoitems(todoid, input):
    """Delete to-do items based on input"""
    return db.execute("UPDATE todoitem SET deleted = True, transacted = :datetime WHERE completed = :input AND todoid = :todoid",
                      input=input, todoid=todoid, datetime=datetime.now())