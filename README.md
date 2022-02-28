# JESSKETCHES WEBSITE
#### Video Demo:  https://www.youtube.com/watch?v=a6cnRCpabnE
#### Description:
The aim of my project was to create a website for my artwork, which would function as a portfolio for future use. For the purposes of this project, my second goal
was to develop a shop within this website, in order to build something more dynamic and complex than a static website. Therefore, my shop was separated into two
main areas; information and artwork, and the shop itself. As I set out designing my website, I did some research on similar websites to get a feel for what I liked
and didn't like aesthetically and navigation wise. This researched helped me develop a theme for the JESSKETCHES website:
- PLAYFUL
- CONTEMPORY
- VIRTUAL ART GALLERY CURATED BY ME
- FULL OF ENERGY/ INSPIRATION UPON VISIT (no pop-ups, too much writing without asking for it)

This theme helped me keep a focused narrative throughout building the website, and guided what new techniques I needed to research, learn and implement.

For this project I created a Flask application using Python, SQLite, HTML, CSS, Jinja and Javascript. I also utilised Bootstrap 5 to assist with the layout of pages.

### Information and Artwork
#### Index
'index.html' is the homepage of JESSKETCHES website. Interactive artwork fills the page in three columns, CSS has been used to invert their colour when hovered
over. When these images are clicked on, the user is taken to the 'Work' page that features that image. At the very top of the page, an image reading 'JESSKETCHES'
followed by a picture of the artist is displayed to introduce the artist. Javascript was used to transform these two images off to the sides of the page as the
user scrolled down to increase the activity and playfulness of the homepage.

There is a navigation bar (navbar) at the top of the page, along with a fixed footer which solely presents an instagram logo linking to the artist's instagram page.
Both navigation bars remain present throughout almost all of the pages, with exceptions such as no instagram footer on the contact page as the same link is presented
in the main content. The top navbar utilises dropdown menus to organise the artist's artwork pages, along with further page links across the top. The logo is in the
top left hand corner to always navigate the user back to the homepage.

As the homepage is very image heavy, a loading page was created with a silly drawing of a grumpy cat along with a sarcastic message 'This better be worth the wait'.
I wanted to keep things playful as per the theme, and hopefully inject a bit of fun into an annoying loading page! This loading page is presented until all content
of the main page has loaded, at which point a Javascript function kicks in an hides the loading content and makes the main page visible.

#### Work
The 'Work' pages are organised into themes, with each page using Bootstrap 5 to support a clean and responsive layout which is mobile first. These pages include
images and text.

#### About Me
To keep with the playful user experience, the 'About Me' page starts with an interactive image of the artist that rolls off the page as the user scrolls down,
this was implemented using Javascript. A different style of text was also used here to encourage a more informal, approachable feel. This page includes images and
text.

#### Contact
The 'Contact' page includes a link to the artist's instagram page and a link to email the artist directly. These again are kept light-hearted with googly eyes and
biro pens popping into view when the contact details are hovered over. When the user clicks on the artist's email, the HTML initiates a new email to jessketches
on the user's device, with the subject line 'JESSKETCHES WEBSITE QUERY :)' using the HTML 'a' tag.

### Shop
When a user enters the 'Shop' page, the navbar includes a further item on the right hand side; the user icon. When clicked on, the user icon presents different
options in a dropdown menu depending on whether the user is logged in or a guest. The links include: log in, log out, register, view basket, view previous shopping
history, and a text reminder of who is logged in using the registered first name. If the user chooses to add any items to their basket for checkout, a shopping cart
icon will also appear in the right hand side of the navbar displaying the number of items in the user's basket. If the shopping cart is clicked on, the user is
taken to their shopping basket summary page. The basket is formatted using CSS, and both the basket and user icon are provided variables from application.py to
keep the display up-to-date using Jinja with if/else statements where needed.

The shop is where the Flask application is really utilised. Here, information is passed to and from the SQLite database via application.py, HTML and Jinja. This keeps
information up-to-date on both the user’s screen and in the database.

The flash function was used in application.py for error checking throughout the shop. An error message will appear at the top of the page if, for example, the user
attempts to submit a form without completing all mandatory boxes, or they exceeded a limit, such as the max capacity of 20 copies per item. It is also used at the
end of the checkout process as the user is taken back to the homepage to confirm that the order has been received, and in a similar way when the seller requests a
confirmation of postage email to be sent to the customer, a message will flash up once the task is complete to confirm the email has been sent.

#### The Shop Homepage
The 'Shop' homepage consists of a summary of the work sold, followed by a list of all items within the shop, and a link displayed at the bottom of the page to take
the user to the basket (if they have any items in there!). This basket link was added at the bottom after testing the site with users, as I found some users did not
intuitively click on the shopping cart in the navbar as I had assumed. Each item in the shop includes an image of the artwork which changes to a staged photo of the
item in a home environment when hovered over using CSS, a description of the item, and a form for the user to complete if they choose to add the item to their basket.
The HTML form uses Javascript to display a text box for input of a personalised message on the front of the card if this option is chosen on the drop-down menu. When
a form is submitted, the information passes via application.py to the SQLite database 'basket' table (SQLite pathway will be explained shortly).

#### Basket
When the user opens the 'Basket' page, they are presented with a table displaying a summary of the items within their basket, as per the information held for their
session user id in the SQLite database. There is an option to add or remove some or all copies of each item, this has been limited to 20 copies per item in
application.py. If selected, the user's addition/ removal will be updated in the SQLite database. Delivery costs and a total balance to pay are then displayed at the
bottom of the table.

If the user then chooses to checkout, they are offered the following options (unless already logged in): checkout as guest, sign in, or register. Whatever the user
chooses, their basket will remain the same, as the session id is linked to the items in their basket in the SQLite database 'basket' table.

#### Checkout
Once the user has chosen whether to checkout as a guest or registered customer, they will be presented with two buttons on a new page - they can either checkout all
items to one address, or checkout items to different addresses and/or add a personalised message to be included inside the card.

If the user chooses to send all items to one address, they are redirected to a page that offers the option of choosing from their registered address via SQLite (if
signed in), or inputting a new address via a form. The user will then be directed to the final checkout page, which is also what the user would have been directed to
if they chose the second option of personalised message/ different addresses.

Originally I built two separate pathways for checkout depending on whether the user chose to checkout all items to the same address or to different addresses/ add
personalised messages. However, I soon realised this was creating an unnecessary amount of pages and could actually be improved if both pathways linked back up. If
the user chose to send all items to one address, the benefit of then making their final confirmation page the same as if the user chose the second option, is that
it still provides the same summary information they would have had on their own unique final checkout page, but also gave the user a chance to edit any postal
information or add a personalised message if they made a mistake or changed their mind. This took some re-jigging of how information was being sent and received to
each page, but resulted in a more efficient checkout process.

This final checkout page either allows for edits or first time entries to addresses and/or personalised messages, with one form per item in the basket. These forms
add/ renew information in the SQLite database via application.py.

Once the user is happy with the checkout details
they are able to checkout using the Paypal options (including Paypal, SOFORT, or Debit/ Credit Card). The payment segment uses Paypal's Javascript which was
slightly edited by myself to fit my requirements. If I were to do this again, I would have looked into the payment structure I was going to use a lot earlier in
the development process, as by the time I came to research payments, I had already created my own shopping structure up to and including sending out confirmation
emails to the customer and seller. I since realised a lot of this was automated with Paypal, and therefore I had to amend their code to fit my pre-existing work
flow. If I were to make this shop go live, I would probably amend my code and leave Paypal’s code untouched to ensure the payment was secure and taken as intended
by Paypal’s Javascript.

The two areas of Paypal’s javascript that I edited for the purposes of this project were:
- passing in the total value of the basket from my code, instead of registering items and their prices on the structured Paypal system for Paypal to total
- passing the information back into application.py via a POST request when payment has been accepted, instead of finalising the order straight away. This is so
that I could update the SQLite database, send out a personalised confirmation email to the customer and the seller using flask_mail, and to redirect the customer
to JESSKETCHES homepage after their order. Paypal also send a confirmation email to the buyer, so this could have been utilised had I researched this earlier in
the process. Having said that, for learning purposes I am grateful it worked out the way it did, as I was able to learn more about flask_mail than I would have
had I leant on Paypal's process.

#### Sign in/ Register/ Logout
As soon as a user enters the 'Shop' page, a session user id is assigned to log shopping basket activity, the id is generated using uuid4(). This session id will
be updated to the registered user id if the user subsequently signs in.

There are individual pages to sign in and register, along with forms at checkout which will also complete the same function for sign-in. Registration includes
providing an email address which doubles up as the username, a password and confirmation of the password, and their name and postal address for future orders.
The password is hashed before being entered into the SQLite database for security. As mentioned before, flash messages are used to notify the user of any
issues when error checking such as; an empty field in a form upon submission, or an unknown username/ password being entered when signing in.

Logging out will clear any session user id's, create a new guest user id, and redirect the user to the homepage.

#### View Shopping History
Whilst logged in, the user has the option of viewing their shopping history. This pulls information from SQLite of any previous completed purchases by
this user via their session user id. Information presented includes the order reference, postal address, purchase date and summary of the order in a table
similar to the checkout summary table.

#### Seller Page
The seller has their very own page which is hidden from customers. This page is only accessible via a direct link, and is not linked at all from the main
JESSKETCHES website. This link would be included in the order confirmation email each time an order is made. Upon opening the link, the seller needs to input
a username and password which is pre-defined by the seller with the web developer.

Upon logging in, the seller can view all current orders that are due to be shipped, and once they have posted these out, they can press a button to confirm
the items have been posted. This button then automatically sends a personalised email to the customer to confirm their item is on its way, and updates the
SQLite database with the current date and time under the postage check column. The seller will then see a flash message to congratulate them on another order
posted out, which will also confirm that the email has been sent to the customer.

The seller can also view historical orders on this page, just below the current orders due to be posted.

If by some chance a user guesses the hidden URL for the seller's order list, the user will be redirected to the homepage as application.py will confirm the seller
is logged in with the correct credentials before allowing access to this part of the site.

#### Apology page
If an error occurs which has not been accounted for (and hence no flash message is prepared in advance), the errorhandler function will return an apology page
created to inform the user that something has gone wrong. The user can then chose from the navbar where they would like to return to. There is a silly drawing
of a grumpy cat on this apology page, to keep things playful!

### SQLite Database
The SQLite database has the following schema:
```
CREATE TABLE IF NOT EXISTS 'registered' ('id' text PRIMARY KEY NOT NULL,'email' text NOT NULL, 'hash' text NOT NULL, 'country'  text NOT NULL  , 'full_name'  text NOT NULL  , 'street_number_name'  text NOT NULL  , 'street'  text NOT NULL  , 'city'  text NOT NULL  , 'postcode'  text NOT NULL  );
CREATE TABLE IF NOT EXISTS 'guest' ('guest_user_id' text NOT NULL, 'guest_name' text NOT NULL, 'guest_email' text NOT NULL);
CREATE TABLE IF NOT EXISTS 'basket' ('reference' integer PRIMARY KEY AUTOINCREMENT NOT NULL,'user_id' text NOT NULL, 'timestamp' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 'item_name' text NOT NULL, 'item_option' text NOT NULL, 'item_front_text' text NOT NULL DEFAULT 'Blank', 'item_internal_text' text NOT NULL DEFAULT 'Blank', 'cost' real NOT NULL, 'quantity' integer NOT NULL, 'total_cost'  real NOT NULL  , 'checkout_complete' integer NOT NULL DEFAULT 0, 'img_src'  text NOT NULL  );
CREATE TABLE IF NOT EXISTS 'temp_basket' ('tb_reference'  integer PRIMARY KEY NOT NULL  , 'tb_user_id'  text NOT NULL  , 'full_name'  text NOT NULL  , 'street_number_name'  text NOT NULL  , 'street'  text NOT NULL  , 'city'  text NOT NULL  , 'postcode'  text NOT NULL  , 'country'  text NOT NULL  );
CREATE TABLE IF NOT EXISTS 'checkout' ('card_references' text NOT NULL,'checkout_user_id' text NOT NULL, 'timestamp' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 'full_name' text NOT NULL, 'country' text NOT NULL, 'street_number_name' text NOT NULL, 'street' text NOT NULL, 'city' text NOT NULL, 'postcode' text NOT NULL, 'delivery' real NOT NULL, 'discount' text NOT NULL DEFAULT 'None', 'reduction' real NOT NULL DEFAULT 0, 'total_paid'  real NOT NULL  , 'confirmation_sent' integer NOT NULL DEFAULT 0,'posted' datetime NOT NULL DEFAULT 0, 'checkout_reference'  text NOT NULL  , 'checkout_email'  text NOT NULL  );
CREATE TABLE IF NOT EXISTS 'seller' ('id' integer PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' text NOT NULL, 'hash_password' text NOT NULL);

CREATE UNIQUE INDEX 'index_id' ON "registered" ("id" ASC) WHERE id;
CREATE UNIQUE INDEX 'index_email' ON "registered" ("email") WHERE email;
CREATE UNIQUE INDEX 'index_reference' ON "basket" ("reference" ASC) WHERE reference;
CREATE INDEX 'index_user_id' ON "basket" ("user_id") WHERE user_id;
CREATE UNIQUE INDEX 'index_tb_reference' ON "temp_basket" ("tb_reference" ASC) WHERE tb_reference;
CREATE INDEX 'index_tb_user_id' ON "temp_basket" ("tb_user_id" ASC) WHERE tb_user_id;
CREATE UNIQUE INDEX 'index_username' ON "seller" ("username" ASC) WHERE username;
CREATE UNIQUE INDEX 'index_guest_user_id' ON "guest" ("guest_user_id") WHERE guest_user_id;
CREATE INDEX 'index_checkout_complete' ON "basket" ("checkout_complete" ASC);
CREATE UNIQUE INDEX 'index_card_references' ON "checkout" ("card_references" DESC);
CREATE INDEX 'index_checkout_user_id' ON "checkout" ("checkout_user_id");
CREATE INDEX 'index_confirmation_sent' ON "checkout" ("confirmation_sent" ASC);
CREATE INDEX 'index_posted' ON "checkout" ("posted" ASC);
CREATE UNIQUE INDEX 'index_checkout_reference' ON "checkout" ("checkout_reference");
```

When a user registers with JESSKETCHES for a shopping account, their email address, a hashed version of their password, and their postal details are added to
the 'registered' table along with their user id. This user id will now be used as their session id whenever they are logged into this site.

If a user chooses to shop as a guest, only their session id, name and email are saved in the 'guest' table for use in finalising their order.

When a user adds an item to their basket, logged in or not, the item is added to the 'basket' table along with their user id aka session id and a unique
reference number (auto incremental with each addition to the basket). This user id may be updated in the 'basket' table to a registered user id if the user
begins shopping as a guest and later logs in to their account.

When the user is ready to checkout and starts inputting the postal address(es) for their orders, each unique item reference number is added to the 'temp_basket'
table with its correlating postal address and user id, this is then ready for inputting into the 'checkout' table once the order has been confirmed. If the user
chooses to add a personalised message to be placed inside the card, this text will be added to the relevant item in the 'basket' table under 'item_internal_text'.

When the user inputs their payment details and checks out, the order is then added to the 'checkout' table, with all items going to the same address combined
into one row (using a comma separated list of the unique item reference numbers). Every row in the 'checkout' table also includes the postal address, final
costs involved, a check for whether the confirmation email has been sent and a check for whether the item(s) have been posted.

Once checkout has been completed and the confirmation emails have been sent:
- The 'basket' table is updated to confirm items have been checked out (this prevents them from appearing in the user's current basket due to basket checks in
  application.py)
- The 'checkout' table is updated to confirm the confirmation emails have been sent out
- The relevant information is removed from the 'temp_basket' and 'guest' tables now that they are no longer required as per data protection regulations (we
  cannot store information that is no longer necessary)

Once the seller logs in and confirms the order has been posted:
- The 'checkout' table is updated to confirm the order has been posted

The 'seller' table simply includes the id, username and hashed password of the seller's log in details, which were agreed with the web developer upon creation.

I chose to separate the shop.db tables in this way to reduce the duplication of information and instead utilise the temporary join option when information from
different tables needed to be joined together. Although I did plan out the tables before implementation, there was still a lot of tweaking whilst I was building
the shop, as I realised there were more efficient ways of working, or that I hadn't quite thought of how the variables would translate onto the webpage. For
example, originally I did not have the 'temp_basket' table, but was adding every item to the checkout table individually as addresses were added. I then noticed
a lot of duplication of information in terms of postal addresses e.g. if one customer ordered ten different items to one address, this was using up ten rows in
the table when it could be compressed into one row. I then created the 'temp_basket' table to hold every item individually as addresses are added/ possibly changed.
Then when the order is finalised and paid for, application.py checks whether the address is the same for one or more items, and when it is, it adds these unique
item reference numbers together in a comma separated list, and then adds this list to the 'card_references' column in the 'checkout' table alongside the relevant
postal address, costs, and checks.I did, however, intentionally choose to keep all lines of the postal address in separate cells in the tables as I thought this
would keep the information more flexible to possible future requests such as organising orders into similar postcodes or searching for orders by city to produce
statistics helpful for future marketing.

### Python
application.py and helpers.py have made use of comments throughout to further explain the details of my code.

### CSS and HTML
All CSS and HTML pages have made use of comments to help the viewer understand the purpose of each segment.

#### Testing Phase
Once the website was complete (in draft form), I observed willing family and friends navigate around the website and purchase items (using the tester info on
Paypal!), and found areas for improvement; some as small as a spelling error, to some more significant pointers. For example, the loading page that has been used
for the homepage was originally also used on the shop homepage. However, when watching others navigate around the site, I realised how often the shop homepage
is opened throughout the shopping process, and even I was getting frustrated just waiting and watching a loading sign over and over again. I removed the loading
page from the shop and although now the user can see the items as they load up, it allows the user to get on with their next aim a little quicker. For example,
they don't need the pink background loaded to read the item description or add an item to the basket. The sacrifice of a complete presentation seemed worthwhile
here. Furthermore, as the top content seemed to load first, the loading process was not always that visible depending on how quick the device and user were to
scroll down the page. This was an ongoing challenge of having an image heavy site - something I could not easily avoid with a site specifically designed to
celebrate artwork and imagery!

### Reflections (cheese warning)
Overall, I am very pleased with the final product. As a complete novice, this website is far beyond how much I expected to be capable of at the end of CS50,
but the course really does prepare the learner in concepts and questioning. This facilitates the learner to be able to continue self-guided research that is
specifically needed for individual projects.

This is the best course I have ever taken, so jammed packed with information presented intelligently in the most creative and fun ways. There was not five
minutes within all the content that I could call unnecessary. I will forever be grateful to all the staff at CS50 for introducing me to a new passion and
hopefully future career. My plan now is to attend either a coding bootcamp or join an apprenticeship in the UK to be able to gain a junior software developer
role in the future.

My name is Jess, and this has been CS50.