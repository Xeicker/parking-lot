from flask import g
import shelve


class Shelves():
    # Read database, only from file if needed
    @staticmethod
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = shelve.open("cars.db")
        return db


class Car():
    def __init__(self, id, tariff, location, start):
        self.id = id
        self.tariff = tariff
        self.location = location
        self.start = start
        self.finish = None

    def get_as_dict(self):
        """Generates a dictionary from car data"""
        d = {
            "car": self.id,
            "tariff": self.tariff,
            "location": self.location,
            "start": self.start.strftime("%Y-%m-%d %H:%M:%S")}
        if self.finish is not None:
            d["finish"] = self.finish.strftime("%Y-%m-%d %H:%M:%S")
        return d
