from shelve import Shelf
from flask_restful import Resource
from Shelves import get_db
from flask import request
from ParkinLotManager import tariffs,numberofSpots,calculateFee
from webargs.flaskparser import parser
from webargs import fields
from datetime import  datetime

class CarList(Resource):
    def get(self):
        shelf = get_db()
        cars = []
        for key in shelf.keys():
            cars.append(shelf[key])
        return {'message': 'Success', 'data': [x for x in cars if isinstance(x,dict)]}, 200
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
        self.shelf[str(self.spot)] = args["car"]
        return {'message': 'Success', "data": car}, 201
    def validateRequestArguments(self,args):
        if "car" not in args or "tariff" not in args:
            return "Missing arguments on the request"
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
            if str(i) not in self.shelf.keys():
                return i
        return -1
class CarRemove(Resource):
    car_args = {"car": fields.Str(), "location": fields.Str()}
    def get(self):
        self.shelf = get_db()
        args = parser.parse(self.car_args,request,location="query")
        message = self.validateRequestArguments(args)
        if message:
            return {"message" : message} , 400
        fromd = datetime.fromisoformat(self.shelf[self.car]["start"])
        tod = datetime.now()
        fee = calculateFee(fromd,tod,self.shelf[self.car]["tariff"])
        carobj = self.shelf[self.car]
        carobj["finish"] = tod.isoformat()
        del self.shelf[self.car]
        del self.shelf[self.location]
        return {"message" : "Success","fee":fee,"car": carobj},200
    def validateRequestArguments(self,args):
        if "car" not in args and "location" not in args:
            return "Missing arguments"
        elif "car" in args:
            if args["car"] not in self.shelf.keys():
                return "Car not found"
        elif "location" in args:
            if not args["location"].isdigit():
                return "Invalid arguments"
            elif int(args["location"])>=numberofSpots:
                return "Invalid location"
            elif args["location"] not in self.shelf.keys():
                return "Location was free"

        self.car = args["car"] if "car" in args else self.shelf[args["location"]]
        self.location = args["location"] if "location" in args else self.shelf[args["car"]]["location"]
        return ""