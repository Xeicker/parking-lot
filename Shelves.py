from flask import g
import shelve

#Read database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("cars.db")
    return db

