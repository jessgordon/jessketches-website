import os, uuid

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_mail import Mail, Message
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import confirm_login, retrieve_name, item_count, apology

# Configure application
app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("JK_EMAIL")
app.config["MAIL_USERNAME"] = os.getenv("JK_EMAIL")
app.config["MAIL_PASSWORD"] = os.getenv("JK_PASS")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shop.db")


# Global variable for delivery cost per postal address
DELIVERY = 0.99


# Creating routes for all pages that do not require python
@app.route("/")
def index():
    # Assigning the seller logged in status to false in sessions
    # This session will only become true when the seller logs in to their orders page
    session["seller_logged_in"] = 0

    return render_template("index.html")

@app.route("/ACCEPTANCE")
def acceptance():
    return render_template("ACCEPTANCE.html")

@app.route("/C19")
def c19():
    return render_template("C19.html")

@app.route("/COMMISSIONS")
def commissions():
    return render_template("COMMISSIONS.html")

@app.route("/DREAMLAND")
def dreamland():
    return render_template("DREAMLAND.html")

@app.route("/FASHUN")
def fashun():
    return render_template("FASHUN.html")

@app.route("/FLORAL+")
def floral():
    return render_template("FLORAL+.html")

@app.route("/INTERIORS")
def interiors():
    return render_template("INTERIORS.html")

@app.route("/JUSTJUMP")
def justjump():
    return render_template("JUSTJUMP.html")

@app.route("/PEOPLE&PLACES:LONDON")
def peopleplaceslondon():
    return render_template("PEOPLE&PLACES:LONDON.html")

@app.route("/SEABORN")
def seaborn():
    return render_template("SEABORN.html")

@app.route("/SOMEBODIES")
def somebodies():
    return render_template("SOMEBODIES.html")

@app.route("/TATTOO")
def tattoo():
    return render_template("TATTOO.html")

@app.route("/THREAD")
def thread():
    return render_template("THREAD.html")

@app.route("/X(R)PLORATION")
def xrploration():
    return render_template("X(R)PLORATION.html")

@app.route("/ABOUT_ME")
def aboutme():
    return render_template("ABOUT_ME.html")

@app.route("/CONTACT")
def contact():
    return render_template("CONTACT.html")


# Routes for logging in, registering and logging out as a customer in JESSKETCHES shop

@app.route("/LOGIN", methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    ### Log a registered user into their shop account ###

    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            flash('Please input your registered email address.')
            return redirect("/LOGIN")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Please input your password.')
            return redirect("/LOGIN")

        # Query database for email
        rows = db.execute("SELECT * FROM registered WHERE email = ?", request.form.get("email"))

        # Ensure email exists and password is correct
        if len(rows) != 1:
            flash('Invalid email')
            return redirect("/LOGIN")

        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Invalid password')
            return redirect("/LOGIN")

        # Obtain registered user id and current guest id
        registered_user_id = rows[0]["id"]
        guest_user_id = str(session["user_id"])

        # Replace user id in basket from guest user id to the user's registered user
        basket = db.execute("UPDATE basket SET user_id = ? WHERE user_id = ? AND checkout_complete == 0", registered_user_id, guest_user_id)

        # Update session id to registered user id
        session["user_id"] = registered_user_id

        if request.form.get("redirect") == "shop":
            return redirect("/SHOP")
        elif request.form.get("redirect") == "checkout":
            return redirect("/CHECKOUT")

    # User reached route via GET (as by clicking a link or via redirect)
    #### Open the login page ####

    else:

        # Confirming if user currently logged in
        logged_in = confirm_login()

        # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
        name = "empty"
        if logged_in == "yes":
            name = retrieve_name()

        # Calculating items currently in the basket
        item = item_count()

        return render_template("login.html", logged_in=logged_in, name=name, item=item)


@app.route("/LOGOUT")
def logout():
    ### Log current user out ###

    # Forget any session user_id
    session.clear()

    # Create a new guest session id
    if "user_id" not in session:
        user_id = uuid.uuid4()
        session["user_id"] = user_id

    # Redirect user to index
    return redirect("/")


@app.route("/REGISTER", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    ### Register a new user to the JESSKETCHES shop ###

    if request.method == "POST":

        # Error Checking - ensure email was submitted
        if not request.form.get("email"):
            flash('Please provide an email address')
            return redirect("/REGISTER")

        # Error Checking - ensure email does not already exist
        existing_email = db.execute("SELECT * FROM registered WHERE email = ?", request.form.get("email"))
        if len(existing_email) == 1:
            flash('Email already registered')
            return redirect("/REGISTER")

        # Error Checking - ensure password and confirmation of password were submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            flash('Must provide password and confirmation of password')
            return redirect("/REGISTER")

        # Error Checking - ensure password and confirmation of password match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash('Password did not match confirmation of password')
            return redirect("/REGISTER")

        # Error Checking - ensure country was submitted
        elif not request.form.get("country"):
            flash('Please provide your country')
            return redirect("/REGISTER")

        # Error Checking - ensure full name was submitted
        elif not request.form.get("full_name"):
            flash('Please provide your full name')
            return redirect("/REGISTER")

        # Error Checking - ensure street number/ name was submitted
        elif not request.form.get("street_number_name"):
            flash('Please provide your street number and/or name of the property')
            return redirect("/REGISTER")

        # Error Checking - ensure street was submitted
        elif not request.form.get("street"):
            flash('Please provide your street')
            return redirect("/REGISTER")

        # Error Checking - ensure city was submitted
        elif not request.form.get("city"):
            flash('Please provide your city')
            return redirect("/REGISTER")

        # Error Checking - ensure postcode was submitted
        elif not request.form.get("postcode"):
            flash('Please provide your postcode')
            return redirect("/REGISTER")

        # Insert the new user's information into the 'registered' table in the database
        email = request.form.get("email")
        hashed_password = generate_password_hash(request.form.get("password"))
        country = request.form.get("country")
        full_name = request.form.get("full_name")
        street_number_name = request.form.get("street_number_name")
        street = request.form.get("street")
        city = request.form.get("city")
        postcode = request.form.get("postcode")
        user_id = str(session["user_id"])

        db.execute("INSERT INTO registered (id, email, hash, country, full_name, street_number_name, street, city, postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    user_id, email, hashed_password, country, full_name, street_number_name, street, city, postcode)

        # Redirect user to checkout
        return redirect("/BASKET")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Open the register page ###

    else:

        # Confirming if the user is currently logged in
        logged_in = confirm_login()

        # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
        name = "empty"
        if logged_in == "yes":
            name = retrieve_name()

        # Calculating items currently in the basket
        item = item_count()

        return render_template("register.html", logged_in=logged_in, name=name, item=item)


@app.route("/SHOP", methods=["GET", "POST"])
def shop():
    ### Open the shop homepage ###

    # Assigning a session user id to log shopping basket activity - id generated using uuid4()
    if "user_id" not in session:
        user_id = uuid.uuid4()
        session["user_id"] = user_id

    # Defining the quantity range for each card quantity drop-down option (maximum of 20 per print)
    quantity = []
    for i in range(20):
        quantity.append(i+1)

    # Calculating items currently in the basket
    item = item_count()

    # Confirming if user currently logged in
    logged_in = confirm_login()

    # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
    name = "empty"
    if logged_in == "yes":
        name = retrieve_name()

    return render_template("shop.html", quantity=quantity, item=item, logged_in=logged_in, name=name)


@app.route("/submission", methods=["POST"])
def subbmission():
    ### Adding the item the user selected from the shop homepage to their basket ###

    # Error checking - no card option inputted
    if not request.form.get("card_options"):
        flash('Please choose a style option.')
        return redirect("/SHOP")

    # Error checking - no quantity inputted
    if not request.form.get("quantity"):
        flash('Quantity must be at least one unit.')
        return redirect("/SHOP")

    # Error checking - confirm integer inputted
    try:
        quantity = int(request.form.get("quantity"))
    except ValueError:
        flash('Quantity must be a whole number.')
        return redirect("/SHOP")

    # Error checking - confirm quantity is a positive integer and within the allocated range
    if quantity < 1 or quantity > 20:
        flash('Please insert at least one unit in quantity, max 20 units per print.')
        return redirect("/SHOP")

    # Error checking - not more than 20 orders per print per checkout
    item_name = request.form.get("id")
    user_id = str(session["user_id"])
    current_quantity = db.execute("SELECT SUM(quantity) FROM basket WHERE item_name = ? AND user_id = ? AND checkout_complete == 0", item_name, user_id)
    current_quantity = current_quantity[0]["SUM(quantity)"]
    if current_quantity:
        if (int(current_quantity) + quantity) > 20:
            flash('Please note there is a maximum of 20 units per print, for larger orders please feel free to email JESSKETCHES via the contact page.')
            return redirect("/SHOP")

    # Error checking - if print plus chosen, but no personalised message
    if request.form.get("card_options") == "print_plus" and not request.form.get("personalised_message"):
        flash("Please insert personalised text for the front of the card, or change your style option to 'Print'.")
        return redirect("/SHOP")

    # Insert the user's selection into the basket database
    item_option = request.form.get("card_options")
    item_front_text = "Blank"
    if item_option == "print_plus":
        item_front_text = request.form.get("personalised_message")
    quantity = request.form.get("quantity")
    cost = request.form.get("cost")
    total_cost = int(quantity) * float(cost)
    img_src = request.form.get("img_src")

    db.execute("INSERT INTO basket (user_id, item_name, item_option, item_front_text, cost, quantity, total_cost, img_src) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                user_id, item_name, item_option, item_front_text, cost, quantity, total_cost, img_src)

    return redirect("/SHOP")


@app.route("/BASKET", methods=["GET", "POST"])
def basket():

    # User reached route via POST (as by submitting a form via POST)
    ### Multiplying or removing items from the user's basket as requested by the user ###

    if request.method == "POST":

        if request.form.get("amount_add"):

            # Error checking - confirm integer inputted
            try:
                amount = int(request.form.get("amount_add"))
            except ValueError:
                flash('Quantity must be a whole number.')
                return redirect("/BASKET")

            # Error checking - confirm quantity is a positive integer and within the allocated range
            if amount < 1 or amount > 20:
                flash('Please insert at least one numerical unit in quantity, max 20 units per print.')
                return redirect("/BASKET")

            # Error checking - not more than 20 orders per print per checkout
            item_name = request.form.get("item_name")
            user_id = str(session["user_id"])
            current_quantity = db.execute("SELECT SUM(quantity) FROM basket WHERE item_name = ? AND user_id = ? AND checkout_complete == 0", item_name, user_id)
            current_quantity = current_quantity[0]["SUM(quantity)"]
            new_quantity = int(current_quantity) + amount
            if new_quantity > 20:
                flash('Please note there is a maximum of 20 units per print, for larger orders please feel free to email JESSKETCHES via the contact page.')
                return redirect("/BASKET")

            # Inserting the user's requested addition into the basket database - i.e. updating quantity and total cost
            reference = request.form.get("reference")
            cost = request.form.get("cost")
            quantity_ref = db.execute("SELECT quantity FROM basket WHERE reference = ?", reference)
            quantity_ref = int(quantity_ref[0]["quantity"])
            new_quantity_ref = int(quantity_ref + amount)
            total_cost = float(cost) * new_quantity_ref
            db.execute("UPDATE basket SET quantity = ?, total_cost = ? WHERE reference = ?", new_quantity_ref, total_cost, reference)

            return redirect("/BASKET")

        elif request.form.get("amount_remove"):

            # Error checking - confirm integer inputted
            try:
                amount = int(request.form.get("amount_remove"))
            except ValueError:
                flash('Quantity must be a whole number.')
                return redirect("/BASKET")

            # Error checking - confirm integer is positive
            if amount < 1:
                flash('Please insert at least one numerical unit in quantity.')
                return redirect("/BASKET")

            # Updating the basket database to reflect the user's requested removal - updating quantity and total cost
            reference = request.form.get("reference")
            current_quant_ref = db.execute("SELECT quantity FROM basket WHERE reference = ?", reference)
            current_quant_ref = int(current_quant_ref[0]["quantity"])
            new_quantity = int(current_quant_ref - amount)
            if new_quantity < 0:
                new_quantity = 0
            if new_quantity == 0:
                db.execute("DELETE FROM basket WHERE reference = ?", reference)
            else:
                cost = float(request.form.get("cost"))
                total_cost = new_quantity * cost
                db.execute("UPDATE basket SET quantity = ?, total_cost = ? WHERE reference = ?", new_quantity, total_cost, reference)

            return redirect("/BASKET")

        # If no add or remove amount was inputted but button pressed, do not action
        else:

            return redirect("/BASKET")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Open the shopping basket page ###

    else:

        # Calculating items currently in the basket and redirecting to the shop homepage if the basket is empty
        item = item_count()
        if not item:
            return redirect("/SHOP")

        # Obtaining items currently in the basket
        user_id = str(session["user_id"])
        basket = db.execute("SELECT * FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)

        # Calculating quantity options to add or remove an amount for a specified print (maximum of 20 per print)
        for row in basket:
            item_name = row["item_name"]
            current_quantity = db.execute("SELECT SUM(quantity) FROM basket WHERE item_name = ? AND user_id = ? AND checkout_complete == 0", item_name, user_id)
            current_quantity = int(current_quantity[0]["SUM(quantity)"])
            add_quantity = int(20 - current_quantity)
            remove_quantity = int(row["quantity"])

            # Defining amount possible to add per print in list form for the item drop down menu
            row["amount_add"] = []
            for i in range(add_quantity):
                row["amount_add"].append(i+1)

            # Defining amount possible to remove per print in list form for the item drop down menu
            row["amount_remove"] = []
            for i in range(remove_quantity):
                row["amount_remove"].append(i+1)

        # Obtaining total cost of user's basket
        basket_total_dict = db.execute("SELECT SUM(total_cost) FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)
        basket_total = float(basket_total_dict[0]["SUM(total_cost)"])

        # Calculating any discount to be applied (10% Discount for 3 or more cards, 20% Discount for 5 or more cards)
        quantity_total_dict = db.execute("SELECT SUM(quantity) FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)
        quantity_total = int(quantity_total_dict[0]["SUM(quantity)"])

        discount = "none"
        if quantity_total > 4:
            discount = "20%"
        elif quantity_total > 2:
            discount = "10%"

        # Defining a reduction decimal to use in the final total cost calculation
        reduction = 0
        if discount == "10%":
            reduction = 0.1
        elif discount == "20%":
            reduction = 0.2

        # Confirming current delivery price for the UK from the global variable
        delivery = DELIVERY

        # Calculating the final total cost including discounts and delivery
        reduced = reduction * basket_total
        total = basket_total + delivery - reduced

        # Formatting currency related variables into two decimal place floats for use on the webpage
        reduced = "{:.2f}".format(reduced)
        total = "{:.2f}".format(total)
        basket_total = "{:.2f}".format(basket_total)

        for row in basket:
            row["total_cost"] = "{:.2f}".format(float(row["total_cost"]))

        # Confirming if user currently logged in
        logged_in = confirm_login()

        # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
        name = "empty"
        if logged_in == "yes":
            name = retrieve_name()

        return render_template("basket.html", item=item, basket=basket, basket_total=basket_total, discount=discount, reduced=reduced, delivery=delivery, total=total, logged_in=logged_in, name=name)


@app.route("/CHECKOUT", methods=["GET", "POST"])
def checkout():

    # User reached route via POST (as by submitting a form via POST)
    ### Finalise the checkout process after payment has been taken via PayPal ###

    if request.method == "POST":

        user_id = str(session["user_id"])

        # Obtaining items currently in basket and linking on any addresses inputted by user for posting
        basket = db.execute("SELECT * FROM basket LEFT OUTER JOIN temp_basket ON basket.reference=temp_basket.tb_reference WHERE basket.user_id = ? AND basket.checkout_complete == 0", user_id)

        addresses = db.execute("SELECT * FROM temp_basket WHERE tb_user_id = ? GROUP BY full_name, street_number_name, street, city, postcode, country ORDER BY full_name", user_id)
        for i in range(len(addresses)):
            addresses[i]["reference_list"] = "none"
            for j in range(len(basket)):
                if addresses[i]["full_name"] == basket[j]["full_name"] and addresses[i]["street_number_name"] == basket[j]["street_number_name"] and addresses[i]["street"] == basket[j]["street"] and addresses[i]["city"] == basket[j]["city"] and addresses[i]["postcode"] == basket[j]["postcode"] and addresses[i]["country"] == basket[j]["country"]:
                    if addresses[i]["reference_list"] == "none":
                        addresses[i]["reference_list"] = str(basket[j]["reference"])
                    else:
                        addresses[i]["reference_list"] += ", " + str(basket[j]["reference"])

        # Calculating any discount to be applied (10% Discount for 3 or more cards, 20% Discount for 5 or more cards)
        quantity_total_dict = db.execute("SELECT SUM(quantity) FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)
        quantity_total = int(quantity_total_dict[0]["SUM(quantity)"])

        discount = "none"
        if quantity_total > 4:
            discount = "20%"
        elif quantity_total > 2:
            discount = "10%"

        # Defining a reduction decimal to use in the final total cost calculation
        reduction = 0
        if discount == "10%":
            reduction = 0.1
        elif discount == "20%":
            reduction = 0.2

        # Confirming current delivery price for the UK from the global variable
        delivery = DELIVERY

        # Create a unique order number using uuid4()
        order_number = str(uuid.uuid4())

        # Assign user's email address to an email variable
        email = db.execute("SELECT email FROM registered WHERE id = ?", user_id)
        if len(email) == 1:
            email = str(email[0]["email"])
        else:
            email = db.execute("SELECT guest_email FROM guest WHERE guest_user_id = ?", user_id)
            email = str(email[0]["guest_email"])

        # Add discount, delivery, user_id, email and order number to each address row
        for i in range(len(addresses)):
            addresses[i]["discount"] = discount
            addresses[i]["delivery"] = delivery
            addresses[i]["checkout_reference"] = order_number
            addresses[i]["checkout_user_id"] = str(user_id)
            addresses[i]["checkout_email"] = email

        # Calculate total cost per address
        for i in range(len(addresses)):
            refs = addresses[i]["reference_list"].split(", ")
            addresses[i]["total_cost"] = 0.00
            for j in range(len(refs)):
                ref_cost = db.execute("SELECT total_cost FROM basket WHERE reference = ?", refs[j])
                ref_cost = float(ref_cost[0]["total_cost"])
                addresses[i]["total_cost"] += ref_cost
            # Calculating total cost including discounts and delivery per address
            addresses[i]["reduction"] = float(addresses[i]["total_cost"]) * float(reduction)
            addresses[i]["total_cost"] = float(addresses[i]["total_cost"]) + DELIVERY - float(addresses[i]["reduction"])
            # Formatting currency related variables into two decimal place floats for use on the email
            addresses[i]["reduction"] = "{:.2f}".format(addresses[i]["reduction"])
            addresses[i]["total_cost"] = "{:.2f}".format(addresses[i]["total_cost"])
        # Formatting currency related variables into two decimal place floats for use on the email
        for row in basket:
            row["total_cost"] = "{:.2f}".format(float(row["total_cost"]))

        # Inputting details into checkout table
        for i in range(len(addresses)):
            db.execute("INSERT INTO checkout (card_references, checkout_user_id, full_name, country, street_number_name, street, city, postcode, delivery, discount, reduction, total_paid, checkout_reference, checkout_email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        addresses[i]["reference_list"], addresses[i]["checkout_user_id"], addresses[i]["full_name"], addresses[i]["country"], addresses[i]["street_number_name"], addresses[i]["street"], addresses[i]["city"], addresses[i]["postcode"], addresses[i]["delivery"], addresses[i]["discount"], addresses[i]["reduction"], addresses[i]["total_cost"], addresses[i]["checkout_reference"], addresses[i]["checkout_email"])

        # Sending confirmation email to user
        message = Message(recipients=[email], reply_to="private@gmail.com")
        message.subject = "Thank you for your purchase! Order Reference:" + str(order_number)

        # Initiating confirmation email to website owner so that they are notified of orders to send out
        seller_msg = Message(recipients=["private@gmail.com"])
        seller_msg.subject = "CONGRATULATIONS you have an order! Order Reference:" + str(order_number)

        # Organising variables required for email:
        # Date
        x = datetime.now()
        date = str(x.strftime("%A") + " " + x.strftime("%d") + " " + x.strftime("%B") + " " + x.strftime("%Y"))

        # Dictionary of items checked out with their postal addresses
        checkout = db.execute("SELECT * FROM checkout WHERE checkout_reference = ?", order_number)

        # Name of the user
        name = db.execute("SELECT full_name FROM registered WHERE id = ?", user_id)
        if len(name) == 1:
            name = str(name[0]["full_name"])
        else:
            name = db.execute("SELECT guest_name FROM guest WHERE guest_user_id = ?", user_id)
            name = str(name[0]["guest_name"])

        # Rendering html for the email to be sent to the user
        message.html = render_template("checkout_email.html", date=date, checkout=checkout, name=name, basket=basket)

        # Rendering html for the email to be sent to the seller
        seller_msg.html = render_template("checkout_email_seller.html", date=date, checkout=checkout, name=name, basket=basket)

        # Attaching all images to be used in both emails - including only attaching the print images for items that have been ordered
        # If the image key value == '0' it means the image has not yet been attached, once it's value changes to '1' it has been attached,
        # and will not be attached again on the same email to prevent duplicates

        # Attaching relevant print images
        KKCS2019 = 0
        TB2019 = 0
        P2019 = 0
        KKCSW2019 = 0
        LTTYH2019 = 0

        for basket in basket:

            if basket["item_name"] == "KKCS2019" and KKCS2019 == 0:
                with app.open_resource("/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_kings_cross_canal_side.jpeg") as KKCS2019:
                    message.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', KKCS2019.read(), 'inline', headers=[['Content-ID','<KKCS2019>']])
                    KKCS2019.seek(0)
                    seller_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', KKCS2019.read(), 'inline', headers=[['Content-ID','<KKCS2019>']])
                KKCS2019 = 1

            elif basket["item_name"] == "TB2019" and TB2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_phonebox.jpeg') as TB2019:
                    message.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', TB2019.read(), 'inline', headers=[['Content-ID','<TB2019>']])
                    TB2019.seek(0)
                    seller_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', TB2019.read(), 'inline', headers=[['Content-ID','<TB2019>']])
                TB2019 = 1

            elif basket["item_name"] == "P2019" and P2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_paper.jpeg') as P2019:
                    message.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', P2019.read(), 'inline', headers=[['Content-ID','<P2019>']])
                    P2019.seek(0)
                    seller_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', P2019.read(), 'inline', headers=[['Content-ID','<P2019>']])
                P2019 = 1

            elif basket["item_name"] == "KKCS:W2019" and KKCSW2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_P10.jpeg') as KKCSW2019:
                    message.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', KKCSW2019.read(), 'inline', headers=[['Content-ID','<KKCS:W2019>']])
                    KKCSW2019.seek(0)
                    seller_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', KKCSW2019.read(), 'inline', headers=[['Content-ID','<KKCS:W2019>']])
                KKCSW20199 = 1

            elif basket["item_name"] == "LTTYH2019" and LTTYH2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_P13.jpeg') as LTTYH2019:
                    message.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', LTTYH2019.read(), 'inline', headers=[['Content-ID','<LTTYH2019>']])
                    LTTYH2019.seek(0)
                    seller_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', LTTYH2019.read(), 'inline', headers=[['Content-ID','<LTTYH2019>']])
                LTTYH2019 = 1

        # Attaching JESSKETCHES name image
        with app.open_resource('/home/ubuntu/fp/homepage/static/jskname.png') as jskname:
            message.attach('jskname.png', 'image/png', jskname.read(), 'inline', headers=[['Content-ID','<jskname>']])
            jskname.seek(0)
            seller_msg.attach('jskname.png', 'image/png', jskname.read(), 'inline', headers=[['Content-ID','<jskname>']])

        # Attaching instagram logo
        with app.open_resource('/home/ubuntu/fp/homepage/static/instagram-icon.png') as instaicon:
            message.attach('instagram-icon.png', 'image/png', instaicon.read(), 'inline', headers=[['Content-ID','<instaicon>']])
            instaicon.seek(0)
            seller_msg.attach('instagram-icon.png', 'image/png', instaicon.read(), 'inline', headers=[['Content-ID','<instaicon>']])

        # Sending email to user
        try:
            mail.send(message)
        except Exception:
            # Remove items from checkout table as this will need to be reset with correct email address
            # Please note the use of PayPal would have already gone through at this point if this was real life, so the code would need to be
            # altered to reflect the transaction sequence so that the user does not get charged multiple times. The web developer could validate
            # the user's email address earlier on in the user experience i.e. when registering/ logging in/ entering a guest email address.
            # Here, the developer originally created this project without PayPal and then decided to add it in to learn how the PayPal option
            # operates. As this shop will not be used in real life, this issue has been noted but not resolved for this time limited project.
            db.execute("DELETE FROM checkout WHERE checkout_reference = ?", order_number)
            flash("Oops! Something went wrong - it's possible your email address supplied at checkout was invalid. Your transaction has not been processed, please provide a valid email address to proceed.")
            return redirect("/CheckoutToOther")

        # Sending email to seller
        try:
            mail.send(seller_msg)
        except Exception:
            # Remove items from checkout table as this will need to be repeated when trying to checkout again
            # Please note the use of PayPal would have already gone through at this point if this was real life, so the code would need to be
            # altered to reflect the transaction sequence so that the user does not get charged multiple times. The web developer could validate
            # the user's email address earlier on in the user experience i.e. when registering/ logging in/ entering a guest email address.
            # Here, the developer originally created this project without PayPal and then decided to add it in to learn how the PayPal option
            # operates. As this shop will not be used in real life, this issue has been noted but not resolved for this time limited project.
            db.execute("DELETE FROM checkout WHERE checkout_reference = ?", order_number)
            flash("Oops! Something went wrong. Your transaction has not been processed, please try to checkout again.")
            return redirect("/CheckoutToOther")

        # Confirming items checked out in basket table and removing items from temporary basket and guest tables now that emails have been sent successfully
        for i in range(len(addresses)):
            refs = addresses[i]["reference_list"].split(", ")
            for j in range(len(refs)):
                db.execute("UPDATE basket SET checkout_complete = 1 WHERE reference = ?", int(refs[j]))
                db.execute("DELETE FROM temp_basket WHERE tb_reference = ?", int(refs[j]))
        db.execute("DELETE FROM guest WHERE guest_user_id = ?", user_id)

        # Updating checkout table to confirm email sent
        db.execute("UPDATE checkout SET confirmation_sent = 1 WHERE checkout_reference = ?", order_number)

        # Return to homepage and confirm order (via PayPal javascript)
        flash('Thank you for your order, you will recieve a confirmation email shortly.')
        return ("/")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Initiating checkout process taking the user to checkout1.html on 1a step ###
    else:

        # Confirming if user currently logged in
        logged_in = confirm_login()

        # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
        name = "empty"
        if logged_in == "yes":
            name = retrieve_name()

        # Calculating items currently in the basket
        item = item_count()

        checkout = "1a"

        return render_template("checkout1.html", logged_in=logged_in, checkout=checkout, name=name, item=item)


@app.route("/CheckoutAsGuest", methods=["POST"])
def checkoutasguest():

    ### Initiated if user selects to checkout as a guest, and provides their name and email address in the form ###
    ### Updating temporary guest database with user's name and email address and moving the user onto the next stage in the checkout process ####

    # Error checking - confirming name inputted
    if not request.form.get("name"):
        flash("Please provide your full name before proceeding for your order confirmation email")
        return redirect("/BASKET")

    # Error checking - confirming email inputted
    if not request.form.get("email"):
        flash("Please provide your email address before proceeding for your order confirmation email")
        return redirect("/BASKET")

    # Adding guest name and email address to the temporary guest table
    name = request.form.get("name")
    email = request.form.get("email")
    user_id = str(session["user_id"])

    # Removing any name/email address currently stored for this guest from this session so that this information can be updated
    db.execute("DELETE FROM guest WHERE guest_user_id = ?", user_id)

    # Adding new name and email address to temporary guest table
    db.execute("INSERT INTO guest VALUES (?, ?, ?)", user_id, name, email)

    # Confirming if user currently logged in
    logged_in = confirm_login()

    # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
    name = "empty"
    if logged_in == "yes":
        name = retrieve_name()

    # Calculating items currently in the basket
    item = item_count()

    checkout = "1a"

    return render_template("checkout1.html", logged_in=logged_in, checkout=checkout, name=name, item=item)


@app.route("/CheckoutToUser", methods=["GET", "POST"])
def checkouttouser():

    # User reached route via POST (as by submitting a form via POST)
    ### Initiated if user chose to post all items to their address ###
    ### Updates postal address for all items in the users basket and then moves the user onto the next stage in the checkout process ###

    if request.method == "POST":

        user_id = str(session["user_id"])

        user = {}
        # Obtaining postal address for items - here the user selected to use their registered address
        if request.form.get("registered_address") == "yes":
            user = db.execute("SELECT * FROM registered WHERE id = ?", user_id)
            user = user[0]

        # Obtaining postal address for items - here the user selected to use an address they inputted via a form
        else:

            # Error Checking - ensure full name was submitted
            if not request.form.get("full_name"):
                flash('Please provide addressee full name')
                return redirect("/CheckoutToUser")

            # Error Checking - ensure street number/name was submitted
            elif not request.form.get("street_number_name"):
                flash('Please provide addressee street number and/or name of the property')
                return redirect("/CheckoutToUser")

            # Error Checking - ensure street was submitted
            elif not request.form.get("street"):
                flash('Please provide addressee street')
                return redirect("/CheckoutToUser")

            # Error Checking - ensure city was submitted
            elif not request.form.get("city"):
                flash('Please provide addressee city')
                return redirect("/CheckoutToUser")

            # Error Checking - ensure postcode was submitted
            elif not request.form.get("postcode"):
                flash('Please provide addressee postcode')
                return redirect("/CheckoutToUser")

            # Error Checking - ensure country was submitted
            elif not request.form.get("country"):
                flash('Please provide addressee country')
                return redirect("/CheckoutToUser")

            # Allocating new postal address to key value pairs
            user["full_name"] = request.form.get("full_name")
            user["street_number_name"] = request.form.get("street_number_name")
            user["street"] = request.form.get("street")
            user["city"] = request.form.get("city")
            user["postcode"] = request.form.get("postcode")
            user["country"] = request.form.get("country")

        # Obtain dictionary of items user currently has in their basket to be checked out
        basket = db.execute("SELECT reference FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)

        # Updating the temp basket table to link items in the user's basket to their chosen postal address
        for basket in basket:

            # Removing any items currently in the temp basket for this user in this session so that the updated information can be inputted instead
            db.execute("DELETE FROM temp_basket WHERE tb_reference = ?", basket["reference"])

            # Adding current address details to the temp basket
            db.execute("INSERT INTO temp_basket (full_name, street_number_name, street, city, postcode, country, tb_user_id, tb_reference) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        user["full_name"], user["street_number_name"], user["street"], user["city"], user["postcode"], user["country"], user_id, basket["reference"])

        return redirect("/CheckoutToOther")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Opens the checkout1.html page at it's second stage (1b) where the user has selected to send all their items to their own postal adddress ###
    ### User is presented with a form to complete their postal address, and additionally if they are registered, their registered address will
    # be presented as a one click option for them to select instead of filling out the form ###

    else:

        # Confirming if user currently logged in
        logged_in = confirm_login()

        # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
        name = "empty"
        if logged_in == "yes":
            name = retrieve_name()

        # Calculating items currently in the basket
        item = item_count()

        # If the user is logged in, their registered address will be obtained from the registered table in the database to be presented as an option
        user = []
        if logged_in == "yes":
            user_id = str(session["user_id"])
            log = db.execute("SELECT * FROM registered WHERE id = ?", user_id)
            user = log[0]

        checkout = "1b"

        return render_template("checkout1.html", logged_in=logged_in, checkout=checkout, user=user, name=name, item=item)


@app.route("/CheckoutToOther", methods=["GET", "POST"])
def checkouttother():

    # User reached route via POST (as by submitting a form via POST)
    ### Initiated when a user has chosen to update an item's postal address individually, which provides the additional option of a printed
    # message to be sent with the package e.g. if the user is sending directly to the reciever of a gift.
    ### Updates the postal address +/- message for the individual item in the temp basket table and returns to the checkout page ###

    if request.method == "POST":

        # Error Checking - ensure full name was submitted
        if not request.form.get("full_name"):
            flash('Please provide addressee full name')
            return redirect("/CheckoutToOther")

        # Error Checking - ensure street number/name was submitted
        elif not request.form.get("street_number_name"):
            flash('Please provide addressee street number and/or name of the property')
            return redirect("/CheckoutToOther")

        # Error Checking - ensure street was submitted
        elif not request.form.get("street"):
            flash('Please provide addressee street')
            return redirect("/CheckoutToOther")

        # Error Checking - ensure city was submitted
        elif not request.form.get("city"):
            flash('Please provide addressee city')
            return redirect("/CheckoutToOther")

        # Error Checking - ensure postcode was submitted
        elif not request.form.get("postcode"):
            flash('Please provide addressee postcode')
            return redirect("/CheckoutToOther")

        # Error Checking - ensure country was submitted
        elif not request.form.get("country"):
            flash('Please provide addressee country')
            return redirect("/CheckoutToOther")

        # Assigning postal address +/- message details to variables to be inputted into the temp basket
        reference = request.form.get("reference")
        full_name = request.form.get("full_name")
        street_number_name = request.form.get("street_number_name")
        street = request.form.get("street")
        city = request.form.get("city")
        postcode = request.form.get("postcode")
        country = request.form.get("country")
        message = request.form.get("message")
        user_id = str(session["user_id"])

        # Entering postal address for the selected item into the temp basket table
        db.execute("INSERT INTO temp_basket (full_name, street_number_name, street, city, postcode, country, tb_user_id, tb_reference) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                full_name, street_number_name, street, city, postcode, country, user_id, reference)

        # Updating the message to be posted with the package for the selected item in the basket table
        db.execute("UPDATE basket SET item_internal_text = ? WHERE reference = ?", message, reference)

        return redirect("/CheckoutToOther")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Opens the final checkout page, where user's can view their shopping basket alongside any postal addresses +/- messages already inputted ###
    ### If the user chose to send all items to themselves, all addresses will be pre-filled. If the user chose to send items to different addresses,
    # or add a message to be printed and sent with the package, the address section will have a form to be completed to submit each item's postal
    # address and possible message individually. Submitting this form will take them to the 'POST' part of this route. Once submitted, the address
    # and possible message will be pre-filled on this checkout page ###

    else:

        user_id = str(session["user_id"])

        # Calculating items currently in the basket
        item = item_count()
        if not item:
            return redirect("/SHOP")

        # Obtaining items currently in the basket and linking on any addresses already inputted by the user for posting
        basket = db.execute("SELECT * FROM basket LEFT OUTER JOIN temp_basket ON basket.reference=temp_basket.tb_reference WHERE basket.user_id = ? AND basket.checkout_complete == 0", user_id)

        # Obtaining basket total
        basket_total_dict = db.execute("SELECT SUM(total_cost) FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)
        basket_total = float(basket_total_dict[0]["SUM(total_cost)"])

        # Calculating any discount to be applied (10% Discount for 3 or more cards, 20% Discount for 5 or more cards)
        quantity_total_dict = db.execute("SELECT SUM(quantity) FROM basket WHERE user_id = ? AND checkout_complete == 0", user_id)
        quantity_total = int(quantity_total_dict[0]["SUM(quantity)"])

        # Variable to be used on the website for user's to see
        discount = "none"
        if quantity_total > 4:
            discount = "20%"
        elif quantity_total > 2:
            discount = "10%"

        # Variable to be used in calculations of the final total cost
        reduction = 0
        if discount == "10%":
            reduction = 0.1
        elif discount == "20%":
            reduction = 0.2

        # Verify how many addresses are being used for delivery in order to calculate the delivery cost (set delivery price per address - global variable 'DELIVERY')
        addresses = db.execute("SELECT * FROM temp_basket WHERE tb_user_id = ? GROUP BY full_name, street_number_name, street, city, postcode, country ORDER BY full_name", user_id)
        amount_addresses = len(addresses)
        delivery = int(amount_addresses) * DELIVERY

        # Calculating total cost including discounts and delivery
        reduced = reduction * basket_total
        total = basket_total - reduced + delivery

        # Formatting currency related variables into two decimal place floats for use on the webpage
        reduced = "{:.2f}".format(reduced)
        total = "{:.2f}".format(total)
        basket_total = "{:.2f}".format(basket_total)
        for row in basket:
            row["total_cost"] = "{:.2f}".format(float(row["total_cost"]))

        # Confirming if user currently logged in
        logged_in = confirm_login()

        # If logged in, obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
        name = "empty"
        if logged_in == "yes":
            name = retrieve_name()

        return render_template("checkout2.html", logged_in=logged_in, item=item, basket=basket, basket_total=basket_total, discount=discount, reduced=reduced, delivery=delivery, total=total, name=name)

@app.route("/EditAddress", methods=["POST"])
def editaddress():

    ### Initiated if the user choses to edit a postal address and/or message for a specific item on the final checkout page (checkout2.html) ###
    ### Removes the current address for the specific item from the temp basket table and returns the final checkout page to update address/ message
    # via the item's form ###

    # Obtain the item reference for the item the user has chosen to edit/update the address +/- message
    tb_reference = request.form.get("reference")

    # Remove the current address linked to this item in the temp basket so that this can be later replaced
    db.execute("DELETE FROM temp_basket WHERE tb_reference = ?", tb_reference)

    return redirect("/CheckoutToOther")


@app.route("/LOGINSELLER", methods=["POST", "GET"])
def loginseller():

    # User reached route via POST (as by submitting a form via POST)
    ### Confirms log in details are correct for the seller and, if correct, redirects to the seller's personal orders page ###

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Please input your registered username.')
            return redirect("/LOGINSELLER")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Please input your password.')
            return redirect("/LOGINSELLER")

        # Query seller table for username
        rows = db.execute("SELECT * FROM seller WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            flash('Invalid username')
            return redirect("/LOGINSELLER")

        elif not check_password_hash(rows[0]["hash_password"], request.form.get("password")):
            flash('Invalid password')
            return redirect("/LOGINSELLER")

        # Initiate seller's logged in session
        session["seller_logged_in"] = 1

        return redirect("/SELLER")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Opens up the seller's log in page, which is a 'hidden page' i.e. not accessible by any links on the main website. The link is provided
    # to the seller directly via email every time a purchase is made by a customer and can be favourited by the seller for ease of access ###

    else:

        # Forget any user_id
        session.clear()

        # Render log in page for seller
        return render_template("seller_login.html")


@app.route("/SELLER", methods=["GET", "POST"])
def seller():

    # User reached route via POST (as by submitting a form via POST)
    ### From the seller's orders page, the seller has triggered an email to be sent to the buyer to confirm items have been posted ###

    if request.method == "POST":

        # Update checkout table to items being posted on todays date
        date = str(datetime.now())
        checkout_reference = request.form.get("checkout_reference")
        card_references = request.form.get("card_references")
        checkout_email = request.form.get("checkout_email")
        db.execute("UPDATE checkout SET posted = ? WHERE card_references = ? AND checkout_reference = ? AND checkout_email = ?", date, card_references, checkout_reference, checkout_email)

        # Collect variables needed to send email to buyer to confirm items have been posted
        # Splitting the card references (which is a comma seperated list of unique item references for the cards that are being posted to the address
        # in question) into individual items in a list to be able to access each item's information from the basket table
        items = []
        refs = card_references.split(", ")
        for i in range(len(refs)):
            basket = db.execute("SELECT * FROM basket WHERE reference = ?", refs[i])
            items.append(basket[0])

        # Obtaining the address and cost details from the submitted form and placing them into a dictionary
        addresse = {}
        addresse["full_name"] = request.form.get("full_name")
        addresse["street_number_name"] = request.form.get("street_number_name")
        addresse["street"] = request.form.get("street")
        addresse["city"] = request.form.get("city")
        addresse["postcode"] = request.form.get("postcode")
        addresse["country"] = request.form.get("country")
        addresse["total_paid"] = request.form.get("total_paid")

        # Initiate email
        posted_msg = Message(recipients=[checkout_email])
        posted_msg.subject = "Your order is on its way! Order Reference:" + checkout_reference

        # Prepare html template for email
        posted_msg.html = render_template("posted_email.html", addresse=addresse, items=items, date=date, checkout_reference=checkout_reference)

        # Attaching all images to be used in email - including only attaching the print images for items that have been ordered
        # If the image key value == '0' it means the image has not yet been attached, once it's value changes to '1' it has been attached,
        # and will not be attached again on the same email to prevent duplicates

        # Attaching relevant print images
        KKCS2019 = 0
        TB2019 = 0
        P2019 = 0
        KKCSW2019 = 0
        LTTYH2019 = 0

        for items in items:

            if items["item_name"] == "KKCS2019" and KKCS2019 == 0:
                with app.open_resource("/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_kings_cross_canal_side.jpeg") as KKCS2019:
                    posted_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', KKCS2019.read(), 'inline', headers=[['Content-ID','<KKCS2019>']])
                KKCS2019 = 1

            elif items["item_name"] == "TB2019" and TB2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_phonebox.jpeg') as TB2019:
                    posted_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', TB2019.read(), 'inline', headers=[['Content-ID','<TB2019>']])
                TB2019 = 1

            elif items["item_name"] == "P2019" and P2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_paper.jpeg') as P2019:
                    posted_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', P2019.read(), 'inline', headers=[['Content-ID','<P2019>']])
                P2019 = 1

            elif items["item_name"] == "KKCS:W2019" and KKCSW2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_P10.jpeg') as KKCSW2019:
                    posted_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', KKCSW2019.read(), 'inline', headers=[['Content-ID','<KKCS:W2019>']])
                KKCSW20199 = 1

            elif items["item_name"] == "LTTYH2019" and LTTYH2019 == 0:
                with app.open_resource('/home/ubuntu/fp/homepage/static/WORK/PEOPLE&PLACES-LONDON/PPL_P13.jpeg') as LTTYH2019:
                    posted_msg.attach('PPL_kings_cross_canal_side.jpeg', 'image/jpeg', LTTYH2019.read(), 'inline', headers=[['Content-ID','<LTTYH2019>']])
                LTTYH2019 = 1

        # Attaching JESSKETCHES name image
        with app.open_resource('/home/ubuntu/fp/homepage/static/jskname.png') as jskname:
            posted_msg.attach('jskname.png', 'image/png', jskname.read(), 'inline', headers=[['Content-ID','<jskname>']])

        # Attaching instagram logo
        with app.open_resource('/home/ubuntu/fp/homepage/static/instagram-icon.png') as instaicon:
            posted_msg.attach('instagram-icon.png', 'image/png', instaicon.read(), 'inline', headers=[['Content-ID','<instaicon>']])

        # Sending email
        mail.send(posted_msg)

        # When the email has been sent, the seller will be redirected to the seller's orders page and the below flash message will appear
        flash('Another job well done! Confirmation email has been sent to the buyer.')

        return redirect("/SELLER")

    # User reached route via GET (as by clicking a link or via redirect)
    ### Opens the seller's orders page which lists all orders due to be posted, with the option to confirm an order has been posted, followed by
    # all orders that have been made historically ###

    else:
        # Error checking - if seller is not logged in, redirect to the homepage
        if session["seller_logged_in"] != 1:
            return redirect("/")

        # If seller is logged in, obtain all orders due for posting and all historical orders from the checkout table and return the seller's orders page
        else:
            all_orders = db.execute("SELECT * FROM checkout WHERE confirmation_sent = 1")
            orders_to_post = db.execute("SELECT * FROM checkout WHERE posted = 0 AND confirmation_sent = 1")

        return render_template("seller_hx.html", all_orders=all_orders, orders_to_post=orders_to_post)


@app.route("/BUYER_HX")
def buyer_hx():
    ### Opens the customer's personal purchase history page if the user is logged in to the shop ###

    # Confirming if user is currently logged in, and redirecting to the shop if not currently logged in
    logged_in = confirm_login()
    if logged_in != "yes":
        return redirect("/SHOP")

    # Obtain user's first name to greet them on the account drop down menu on the right hand side of the navbar
    name = retrieve_name()

    # Calculating items currently in the basket
    item = item_count()

    # Obtaining details of all postal addresses items were sent to via checkout table
    user_id = str(session["user_id"])
    addresses = db.execute("SELECT * FROM checkout WHERE checkout_user_id = ? AND confirmation_sent = 1", user_id)

    # Gaining a list for each address of the details for each item sent to that address
    for address in addresses:
        card_references = address["card_references"]
        address["reference_list"] = []
        refs = card_references.split(", ")
        for i in range(len(refs)):
            basket = db.execute("SELECT * FROM basket WHERE reference = ?", refs[i])
            address["reference_list"].append(basket[0])

    return render_template("buyer_hx.html", logged_in=logged_in, addresses=addresses, name=name, item=item)

def errorhandler(e):
    ### In the case of an error that is not caught by the code above, return apology page with the code and name of the error ###
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

### Listen for errors ###
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)