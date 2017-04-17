# All the database stuff is in this file. I put it all here so it's easier to debug when things go wrong.
import sqlite3

from flask import g

from config import DATABASE


# I'm not too sure how this code works. I copy and pasted it from http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# It seems to work so don't think about it too much.
def get_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Get a list of all the emails in the database.
def get_email_list():
    # Get a connection to the database
    connection = get_connection()
    # Get a cursor
    cursor = connection.cursor()
    # Run our query
    query = cursor.execute('select email from users;')
    result = query.fetchall()
    # Always close your connection when you're done
    connection.close()
    # The result comes out of the database like [('email@domain.com',), ('email@domain.com',),] which
    # is a pain to read like `result[0][0]`, so lets make is a normal list like
    # ['email@domain.com', 'email@domain.com',]. Then we read it like `result[0]` to get the first email.
    email_list = [row[0] for row in result]
    return email_list


# Add a user to the database
def add_user(email, password_string):
    # Change the password from a string to bytes. See the README for an explanation
    password_bytes = password_string.decode()
    # Get our connection to the database
    connection = get_connection()
    # Get our cursor
    cursor = connection.cursor()
    # Run our query
    result = cursor.execute('insert into users (email, password) values ("{}", "{}");'.format(email, password_bytes))
    # Committing the query we just ran writes it to the database. You don't have to do this when
    # you're reading data. This is like working on a Word document and clicking the Save button.
    connection.commit()
    # Close your connection when you're done.
    connection.close()
    return result


# Get a user from the database
def get_user(email):
    # Get connection
    connection = get_connection()
    # Get cursor
    cursor = connection.cursor()
    # Run our query.
    query = cursor.execute('select email, password from users where email = "{}";'.format(email))
    result = query.fetchone()
    # Close dat connection
    connection.close()
    # Put the info into a dictionary so it's easy to pull stuff out of it after this function is done.
    user = {
        'username': result[0],
        'hashed_password': result[1],
    }
    return user
