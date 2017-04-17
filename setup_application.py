# This file does the stuff you need when you first want to create the project. Right now it just makes
# a fresh database file.
from app import app
from db_utils import get_connection


# Use our schema.sql file to create a new database.
# This is also copy pasted from http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# Def read that link, it has some real good info.
def init_db():
    with app.app_context():
        db = get_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

print('setting up application')

init_db()

print('setup complete')
