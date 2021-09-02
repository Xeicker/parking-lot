from shelve import Shelf
from flask_restful import Resource
from Shelves import get_db
from flask import request
from ParkinLotManager import tariffs,numberofSpots
from webargs.flaskparser import parser
from webargs import fields
from datetime import date, datetime
class CarList(Resource):
    def get(self):
        shelf = get_db()
        devices = []
        for key in shelf.keys():
            devices.append(shelf[key])
        return {'message': 'Success', 'data': devices}, 200
class CarAdd(Resource):
    car_args = {"car": fields.Str(), "tariff": fields.Str()}
    def get(self):
        self.shelf = get_db()
        args = parser.parse(self.car_args,request,location="query")
        print(args)
        message = self.validateRequestArguments(args)
        if message:
            return {"message" : message} , 400
        car = self.buildCar(args)
        self.shelf[args["car"]] = car
        self.shelf[str(self.spot)] = "Used"
        return {'message': 'Success', "data": car}, 200
    def validateRequestArguments(self,args):
        if "car" not in args or "tariff" not in args:
            return "Missing arguments on the request"+str(args)
        elif len(args["car"])==0 or args["car"].isdigit() or args["tariff"] not in tariffs:
            return "Invalid arguments on the request"
        elif args["car"] in self.shelf.keys():
            return "This car id has already been registered"
        self.spot = self.getSpot()
        if self.spot<0:
            return "Parking lot is full"
        return ""
    def buildCar(self, args):
        return {
            "car": args["car"],
            "tariff": args["tariff"],
            "location": str(self.spot),
            "start": datetime.now().isoformat()
        }
    def getSpot(self):
        for i in range(numberofSpots):
            if str(i) not in self.shelf.keys() or \
                (str(i) in self.shelf.keys() and self.shelf[str(i)] == "Free"):
                return i
        return -1