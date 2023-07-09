from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, rates, usd, generate_color, check_password

# Configure application
app = Flask(__name__)
app.debug = False

app.jinja_env.filters["usd"] = usd


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wallet.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show overview of incomes and expenses"""
    user = session['user_id']
    history = db.execute("SELECT * FROM history WHERE user_id=? AND strftime('%m', date_time)=?",
                       user, date.today().strftime('%m'))
    income = 0
    expense = 0
    labels = []
    data = []
    colors = []
    for item in history:
        labels.append(item['name'])
        data.append(item['value'])
        if item['method'] == "Income":
            colors.append("#00FF00")
            income += item["value"]
        else:
            colors.append("#FF0000")
            expense += item["value"]
    balance = db.execute("SELECT cash FROM users WHERE id=?", user)
    balance = balance[0]["cash"]

    return render_template("index.html", income=income, expense=expense, balance=balance, history=history, labels=labels, data=data, colors=colors)


@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    """Add expenses"""
    user = session["user_id"]
    if request.method == "POST":
        if not request.form.get("expense"):
            return apology("must provide income", 400)

        if not request.form.get("name"):
            return apology("must provide the name of the income", 400)


        value = request.form.get("expense")
        name = request.form.get("name").title()

        if not value.isdigit() and not("-" or "," in value):
            return apology("value must be a number", 400)

        value = float(value)
        cash = db.execute("SELECT cash FROM users WHERE id=?", user)
        cash = cash[0]["cash"]

        if value < 0:
            return apology("value must be greater than 0", 400)
        else:
            db.execute("INSERT INTO expense (user_id, name, value) VALUES(?,?,?)", user, name, value)

            db.execute("INSERT INTO history (user_id, name, value, method, date_time) VALUES(?,?,?,?,?)", user, name, value, "Expense", date.today())

            cash -= value
            db.execute("UPDATE users SET cash=? WHERE id=?", cash, user)

            flash("Expense added.")
            return redirect("/")
    else:
        expenses = db.execute("SELECT * FROM history WHERE user_id=? AND method=? AND strftime('%m', date_time)=?", user, "Expense", date.today().strftime('%m'))

        if expenses:
            labels=[]
            data=[]
            colors=[]
            for expense in expenses:
                labels.append(expense['name'])
                data.append(expense['value'])
                colors.append(generate_color())

            return render_template("expense.html", expense=expense, labels=labels, data=data, colors=colors)

        else:
            return render_template("expense.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = db.execute("SELECT * FROM history WHERE user_id=?",
                      session["user_id"])
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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


@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    """Add incomes"""
    user = session["user_id"]
    if request.method == "POST":
        if not request.form.get("income"):
            return apology("must provide income", 400)

        if not request.form.get("name"):
            return apology("must provide the name of the income", 400)


        value = request.form.get("income")
        name = request.form.get("name").title()

        if not value.isdigit() and not("-" or "," in value):
            return apology("value must be a number", 400)

        value = float(value)
        cash = db.execute("SELECT cash FROM users WHERE id=?", user)
        cash = cash[0]["cash"]

        if value < 0:
            return apology("value must be greater than 0", 400)
        else:
            db.execute("INSERT INTO income (user_id, name, value) VALUES(?,?,?)", user, name, value)

            db.execute("INSERT INTO history (user_id, name, value, method, date_time) VALUES(?,?,?,?,?)", user, name, value, "Income", date.today())

            cash += value
            db.execute("UPDATE users SET cash=? WHERE id=?", cash, user)

            flash("Income added.")
            return redirect("/")
    else:
        incomes = db.execute("SELECT * FROM history WHERE user_id=? AND method=? AND strftime('%m', date_time)=?", user, "Income", date.today().strftime('%m'))

        if incomes:
            labels=[]
            data=[]
            colors=[]
            for income in incomes:
                labels.append(income['name'])
                data.append(income['value'])
                colors.append(generate_color())

            return render_template("income.html", income=incomes, labels=labels, data=data, colors=colors)

        else:
            return render_template("income.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        elif not request.form.get("balance"):
            return apology("must provide starting balance", 400)

        users = db.execute("SELECT * FROM users")
        user = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        balance = request.form.get("balance")

        for name in users:
            if name["username"] == user:
                return apology("username aleady exists", 400)

        if not check_password(password):
            return apology("password must have more than 8 characters, uppercase, lowercase and digit", 400)

        if password != confirmation:
            return apology("the password and the confirmation do not match", 400)

        if not balance.isdigit() and not("-" or "," in balance):
            return apology("value must be a number", 400)

        balance = float(balance)

        if balance < 0:
            return apology("value must be  greater than 0", 400)

        db.execute("INSERT INTO users (username, hash, cash) VALUES(?,?,?)",
                   user, generate_password_hash(password), balance)
        
        flash("Registered")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/conversor", methods=["GET", "POST"])
@login_required
def conversor():
    """Currency conversor"""
    symbols = rates()
    if request.method == "POST":
        base_currency = request.form.get("base_currency")
        target_currency = request.form.get("target_currency")
        base_value = request.form.get("base_value")
        base_value = float(base_value)

        rate = rates(base_currency)

        converted = (base_value / rate[f"{base_currency}"]) * rate[f"{target_currency}"]

        return render_template("conversor.html", symbols=symbols, base=base_currency, target=target_currency, value=base_value, converted=converted)
    else:
        base = None
        target = None
        return render_template("conversor.html", symbols=symbols, base=base, target=target)
