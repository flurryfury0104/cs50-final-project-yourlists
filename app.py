import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, timedelta
from helpers import *



# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.permanent_session_lifetime = timedelta(days=365)
app.secret_key = os.getenv('SECRET_KEY', 'for dev')


# Default form input
default = "Untitled"
page = "home"


@app.route("/")
@login_required
def index():
    """Home page"""

    # Call today's date
    today = date.today()

    # Query and format un-deleted shopping lists
    shoppings = query_shopping_lists()
    format_list(shoppings)

    # Query and format un-deleted to-do lists
    todos = query_todo_lists()
    format_list(todos)

    # Render home page
    return render_template("index.html", shoppings=shoppings, todos=todos, today=today)


@app.route("/addshopping", methods=["POST"])
@login_required
def addshopping():
    """Add a shopping list"""

    # Extract and format inputs
    listname = request.form.get("listname_s")
    duedate = request.form.get("duedate_s")
    if not listname:
        listname = default
    if not duedate:
        duedate = None

    # Insert new list into "shopping" table
    add_shopping_list(listname, duedate)

    # Redirect user to home page
    return redirect("/")


@app.route("/deleteshopping/<int:shoppingid>")
@login_required
def deleteshopping(shoppingid):
    """Delete a shopping list"""

    # Update "shopping" table to reflect shopping list as deleted
    delete_shopping_list(shoppingid)

    # Redirect user to home page
    return redirect("/")


@app.route("/tickshopping/<int:shoppingid>")
@login_required
def tickshopping(shoppingid):
    """Complete a shopping list"""

    # Update "shopping" table to reflect shopping list as completed
    tick_shopping_list(shoppingid)

    # Redirect user to home page
    return redirect("/")


@app.route("/editshopping/<int:shoppingid>", methods=["GET", "POST"])
@login_required
def editshopping(shoppingid):
    """Edit a shopping list"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract inputs
        listname = request.form.get("listname")
        duedate = request.form.get("duedate")
        if not duedate:
            duedate = None

        # Update shopping list details in "shopping" table
        edit_shopping_list(shoppingid, listname, duedate)

        #todo
        page = "home"

        # Render home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Query shopping list details
        shopping_list = query_shopping_list_details(shoppingid)
        listname = shopping_list["listname"]
        duedate = shopping_list["duedate"]

        # Query un-deleted items in shopping list
        items = query_shopping_list(shoppingid)

        #todo
        page = "edit_s"

        # Render editshopping page after an item is updated
        return render_template("editshopping.html", listname=listname, duedate=duedate, items=items, shoppingid=shoppingid, page=page)


@app.route("/addshopitem/<int:shoppingid>", methods=["POST"])
@login_required
def addshopitem(shoppingid):
    """Add a shopping list item"""

    # Extract and format inputs
    itemname = request.form.get("itemname")
    if not itemname:
        itemname = default

    # Insert new list into "shopitem" table
    add_shopping_item(shoppingid, itemname)

    # Redirect to editshopping page after an item is updated
    return redirect(url_for("editshopping", shoppingid=shoppingid))


@app.route("/deleteshopitem/<int:itemid>/<int:shoppingid>")
@login_required
def deleteshopitem(itemid, shoppingid):
    """Delete a shopping list item"""

    # Update "shopitem" table to reflect item as deleted
    delete_shopping_item(itemid)

    # Redirect to editshopping page after an item is updated
    return redirect(url_for("editshopping", shoppingid=shoppingid))


@app.route("/tickshopitem/<int:itemid>/<int:shoppingid>")
@login_required
def tickshopitem(itemid, shoppingid):
    """Complete a shopping list item"""

    # Update "shopitem" table to reflect item as completed
    tick_shopping_item(itemid)

    # Redirect to editshopping page after an item is updated
    return redirect(url_for("editshopping", shoppingid=shoppingid))


@app.route("/addtodo", methods=["POST"])
@login_required
def addtodo():
    """Add a to-do list directly from homepage"""

    # Extract and format inputs
    listname = request.form.get("listname_t")
    duedate = request.form.get("duedate_t")
    if not listname:
        listname = default
    if not duedate:
        duedate = None

    # Insert new list into "to-do" table
    add_todo_list(listname, duedate)

    # Redirect user to home page
    return redirect("/")


@app.route("/deletetodo/<int:todoid>")
@login_required
def deletetodo(todoid):
    """Delete a to-do list"""

    # Update "to-do" table to reflect to-do list as deleted
    delete_todo_list(todoid)

    # Redirect user to home page
    return redirect("/")


@app.route("/ticktodo/<int:todoid>")
@login_required
def ticktodo(todoid):
    """Complete a to-do list"""

    # Update "to-do" table to reflect to-do list as completed
    tick_todo_list(todoid)

    # Redirect user to home page
    return redirect("/")


@app.route("/edittodo/<int:todoid>", methods=["GET", "POST"])
@login_required
def edittodo(todoid):
    """Edit a to-do list"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract inputs
        listname = request.form.get("listname")
        duedate = request.form.get("duedate")
        if not duedate:
            duedate = None

        # Update to-do list details in "to-do" table
        edit_todo_list(todoid, listname, duedate)

        # todo
        page = "home"

        # Render homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        #Call today's date
        today = date.today()

        # Query to-do list details
        todo_list = query_todo_list_details(todoid)
        listname = todo_list["listname"]
        duedate = todo_list["duedate"]

        # Query and format un-deleted items in to-do list
        items = query_todo_list(todoid)
        format_list(items)

        page = "edit_t"

        # Render edittodo page after an item is updated
        return render_template("edittodo.html", listname=listname, duedate=duedate, items=items, todoid=todoid, today=today, page=page)


@app.route("/addtodoitem/<int:todoid>", methods=["POST"])
@login_required
def addtodoitem(todoid):
    """Add a to-do list item"""

    # Extract and format inputs
    duedate = request.form.get("duedate_t")
    itemname = request.form.get("itemname")
    if not itemname:
        itemname = default
    if not duedate:
        duedate = None

    # Insert new list into "todoitem" table
    add_todo_item(todoid, itemname, duedate)

    # Render edittodo page after an item is updated
    return redirect(url_for("edittodo", todoid=todoid))


@app.route("/deletetodoitem/<int:itemid>/<int:todoid>")
def deletetodoitem(itemid, todoid):
    """Delete a to-do list item"""

    # Update "todoitem" table to reflect item as deleted
    delete_todo_item(itemid)

    # Render edittodo page after an item is updated
    return redirect(url_for("edittodo", todoid=todoid))


@app.route("/ticktodoitem/<int:itemid>/<int:todoid>")
@login_required
def ticktodoitem(itemid, todoid):
    """Complete a to-do list item"""

    # Update "todoitem" table to reflect item as completed
    tick_todo_item(itemid)

    # Render edittodo page after an item is updated
    return redirect(url_for("edittodo", todoid=todoid))


@app.route("/del_cplt_shoppinglist", methods=["POST"])
@login_required
def del_cplt_shoppinglist():
    """Delete completed shopping lists"""

    # Update "shopping" table to reflect completed shopping lists as deleted
    delete_shoppinglists(True)

    # Redirect user to home page
    return redirect("/")


@app.route("/del_all_shoppinglist", methods=["POST"])
@login_required
def del_all_shoppinglist():
    """Delete all shopping lists"""

    # Update "shopping" table to reflect all shopping lists as deleted
    delete_shoppinglists(True)
    delete_shoppinglists(False)

    # Redirect user to home page
    return redirect("/")


@app.route("/del_cplt_shoppingitem/<int:shoppingid>", methods=["POST"])
@login_required
def del_cplt_shoppingitem(shoppingid):
    """Delete completed shopping list items"""

    # Update "shopitem" table to reflect completed items as deleted
    delete_shoppingitems(shoppingid, True)

    # Redirect to editshopping page after items are updated
    return redirect(url_for("editshopping", shoppingid=shoppingid))


@app.route("/del_all_shoppingitem/<int:shoppingid>", methods=["POST"])
@login_required
def del_all_shoppingitem(shoppingid):
    """Delete all shopping list items"""

    # Update "shopitem" table to reflect all items as deleted
    delete_shoppingitems(shoppingid, True)
    delete_shoppingitems(shoppingid, False)

    # Redirect to editshopping page after items are updated
    return redirect(url_for("editshopping", shoppingid=shoppingid))


@app.route("/del_cplt_todolist", methods=["POST"])
@login_required
def del_cplt_todolist():
    """Delete completed to-do lists"""

    # Update "to-do" table to reflect completed to-do lists as deleted
    delete_todolists(True)

    # Redirect user to home page
    return redirect("/")


@app.route("/del_all_todolist", methods=["POST"])
@login_required
def del_all_todolist():
    """Delete all to-do lists"""

    # Update "to-do" table to reflect all to-do lists as deleted
    delete_todolists(True)
    delete_todolists(False)

    # Redirect user to home page
    return redirect("/")


@app.route("/del_cplt_todoitem/<int:todoid>", methods=["POST"])
@login_required
def del_cplt_todoitem(todoid):
    """Delete completed to-do list items"""

    # Update "todoitem" table to reflect completed items as deleted
    delete_todoitems(todoid, True)

    # Redirect to edittodo page after items are updated
    return redirect(url_for("edittodo", todoid=todoid))


@app.route("/del_all_todoitem/<int:todoid>", methods=["POST"])
@login_required
def del_all_todoitem(todoid):
    """Delete all to-do list items"""

    # Update "todoitem" table to reflect all items as deleted
    delete_todoitems(todoid, True)
    delete_todoitems(todoid, False)

    # Redirect to edittodo page after items are updated
    return redirect(url_for("edittodo", todoid=todoid))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("missing username", 400)

        # Query database for username, ensure username does not exist yet
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        if len(rows) != 0:
            return apology("username is not available", 400)

        # Ensure matching password and confirmation were submitted
        if not password:
            return apology("missing password", 400)
        if not confirmation:
            return apology("missing password confirmation", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Insert new user into "users" table
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashpw)",
                   username=username, hashpw=generate_password_hash(password))

        # Log in and remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract inputs
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("missing username", 400)

        # Ensure password was submitted
        if not password:
            return apology("missing password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """Change user's password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Extract inputs
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure old password was submitted
        if not current_password:
            return apology("missing current password", 400)

        # Query database for existing password hash
        hash_current_password = db.execute("SELECT * FROM users WHERE id = :user_id",
                                           user_id=session["user_id"])[0]["hash"]

        # Ensure old password is correct
        if not check_password_hash(hash_current_password, current_password):
            return apology("current password is incorrect", 400)

        # Ensure matching new password and confirmation were submitted
        if not new_password:
            return apology("missing new password", 400)
        if not confirmation:
            return apology("missing new password confirmation", 400)
        if new_password != confirmation:
            return apology("new password and confirmation do not match", 400)

        # Hash new password
        hash_new_password = generate_password_hash(new_password)

        # Ensure new password is not same as old password
        if check_password_hash(hash_current_password, new_password):
            return apology("new password matches current password, please choose a different new password", 400)

        # Change password
        db.execute("UPDATE users SET hash = :hash_new_password WHERE id = :user_id",
                   hash_new_password=hash_new_password, user_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepw.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)