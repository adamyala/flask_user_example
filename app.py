# This file is where most of the magic happens. Typically in a Flask project you name the main
# Flask file `app.py`

# First, import everyone and their mother
# bcrypt is the module we're using to do password hashing
import bcrypt
from flask import Flask, request, redirect, url_for, render_template
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from db_utils import add_user, get_user, get_email_list
from models import User

# Create the variable that holds all our Flask info
app = Flask(__name__)
# Set our secret key. This is explained in the README
app.secret_key = 'super secret string'

# Most Flask plugins follow the below pattern. We create the `app` variable above.
# Then we pass it into the plugin. Don't think about it too much. Once you use more
# Flask plugins you'll see this happen all the time.
login_manager = LoginManager()
login_manager.init_app(app)


# This snippet of code is run whenever someone who is not logged in tries to access a url
# that requires login. Why is it a decorator? If it wasn't we'd have to add some code to the end
# of every route that handles unauthorized people. If we add it in this decorator then the
# Flask-Login plugin will automatically apply it for routes when someone is not logged in.
# Anything can be returned here. I'm lazy so I'm returning a string. You can use `render_template` if you want.
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


# For most sites, after you log in they give you a session id or a cookie or some other crazy stuff.
# We want something simple. This uses a decorator like the snippet above. If your email is not in the
# database, or if you have no email, then you're not a user.
@login_manager.user_loader
def user_loader(email):
    email_list = get_email_list()

    if email not in email_list:
        return

    user = User()
    user.id = email
    return user


# The signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # If someone is GETing the page, just give them the signup form.
    if request.method == 'GET':
        return render_template('signup_form.html')

    # If someone is POSTing, lets grab their info from the form.
    email = request.form['email']
    password = request.form['password']

    # IMPORTANT: Hashing a password happens in bytes. In python a byte is a type like int, str, and dict
    # It's not important to know how to work with bytes. Just remember that to go from str -> bytes,
    # we use the .encode() method
    password_in_bytes = password.encode()
    # Take their plain password and hash it. For a rundown on hashing, see the README.
    hashed_password = bcrypt.hashpw(password_in_bytes, bcrypt.gensalt())
    # Add the user to the database.
    add_user(email, hashed_password)

    # Our goal is to use the `login_user` function to log someone in. That function takes in
    # a `User` object, so we have to make that first.
    user = User()
    # Flask-Login sometimes wants the `id` to be the `email`. I have no idea why, but it breaks
    # when this line isn't here. Don't think about it too much.
    user.id = email
    # Finally we can log the user in.
    login_user(user)
    # Send them to whatever url you want.
    return redirect(url_for('protected'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Same as signup. If they are GETing, just give them the form.
    if request.method == 'GET':
        return render_template('login_form.html')

    # If it's a POST, get their email and password from the form.
    email = request.form['email']
    password = request.form['password']

    # Use their email to get their info from the database.
    result = get_user(email)
    # If we don't find them, tell them they did something wrong.
    if not result:
        return 'Bad login'

    # Like above, the password has to be in bytes before we hash
    password_in_bytes = password.encode()
    # Check their password. For more info on what's going on here, check the README.
    is_correct_password = bcrypt.checkpw(password_in_bytes, result['hashed_password'].encode())
    # If the password match, log them in. To understand why we're using the `login_user` function,
    # see the signup route's comments above.
    if is_correct_password:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('protected'))
    else:
        return 'Bad login'


@app.route('/protected')
# The `login_required` decorator is awesome. You put it on a route and it will automatically
# check to see if someone is logged in. If they aren't it uses the `unauthorized_handler` above
# to route them somewhere else.
@login_required
def protected():
    return 'Logged in as: ' + current_user.id


# This route runs the `logout_user` function. It logs the user out.
@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
