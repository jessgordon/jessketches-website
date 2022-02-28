import os, requests, urllib.parse

from cs50 import SQL
from flask import Flask, session, redirect, render_template, request
from flask_session import Session
from functools import wraps


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shop.db")


# Confirming if user currently logged in
def confirm_login():

    user_id = str(session["user_id"])
    log = db.execute("SELECT * FROM registered WHERE id = ?", user_id)
    logged_in = "no"
    if len(log) == 1:
        logged_in = "yes"

    return logged_in

# If user is logged in, obtain their first name to greet them on the account drop down menu on the right hand side of the navbar
def retrieve_name():

    user_id = str(session["user_id"])
    full_name = db.execute("SELECT full_name FROM registered WHERE id = ?", user_id)
    full_name = str(full_name[0]["full_name"])
    name_list = full_name.split(" ")
    name = name_list[0]

    return name

# Calculating items currently in the basket
def item_count():

    user_id = str(session["user_id"])
    items = db.execute("SELECT SUM(quantity) FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)
    items = items[0]["SUM(quantity)"]

    return items

# Renders an apology page when an error has occured that did not have a resolution within the main code - the page offers an error code and name for
# user's information
def apology(message, code=400):

    # Escape special characters
    def escape(s):

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)

        return s

    return render_template("apology.html", top="oops, something went wrong!", bottom=(str(code) + ": " + escape(message))), code