from functools import wraps
from flask import redirect, render_template, request, session
import random
import requests



def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def rates(symbol=None):
    """Look up for exchange rates."""
    api_key = "32ae30877f7d8b6c946a8aa6a19deb29"
    if symbol is None:
        try:
            url = f"http://api.exchangeratesapi.io/v1/symbols?access_key={api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return None

        try:
            data = response.json()
            return data["symbols"]

        except (KeyError, TypeError, ValueError):
            return None

    else:
        try:
            url = f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return None

        try:
            data = response.json()
            return data["rates"]

        except (KeyError, TypeError, ValueError):
            return None


def generate_color():
    """Generate a random color."""
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)

    # Construct the color string in the format "#RRGGBB"
    color = f"#{r:02x}{g:02x}{b:02x}"

    return color

def usd(value):
    return f"${value:,.2f}"


def check_password(password):
    lowercase = False
    uppercase = False
    digit = False
    lenght = False

    for char in password:
        if char.islower():
            lowercase = True
        elif char.isupper():
            uppercase = True
        elif char.isdigit():
            digit = True

    if len(password) >= 8:
        lenght = True

    return lowercase and uppercase and digit and lenght
