from shelve import Shelf
from flask_restful import Resource
from Shelves import get_db
from flask import request
from ParkinLotManager import tariffs,numberofSpots,calculateFee
from webargs.flaskparser import parser
from webargs import fields
from datetime import  datetime

class CarList(Resource):
    car_add_args = {"car": fields.Str(), "tariff": fields.Str()}
    def get(self):
        shelf = get_db()
        cars = []
        for key in shelf.keys():
            cars.append(shelf[key])
        return {'message': 'Success', 'data': [x for x in cars if isinstance(x,dict)]}, 200
    def post(self):
        self.shelf = get_db()
        args = parser.parse(self.car_add_args,request,location="json")
        message = self.validatePostRequestArguments(args)
        if message:
            return {"message" : message} , 400
        car = self.buildCar(args)
        self.shelf[args["car"]] = car
        self.shelf[str(self.spot)] = args["car"]
        return {'message': 'Success', "data": car}, 201
    def validatePostRequestArguments(self,args):
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
class Car(Resource):
    def delete(self,identifier):
        self.shelf = get_db()
        message = self.validateDeleteRequestArguments(identifier)
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
    def validateDeleteRequestArguments(self,identifier):
        if len(identifier)==0:
            return "Missing identifier"
        #if identifier is not parseable to integer then it is taken as car ID
        elif not identifier.isdigit():
            if identifier not in self.shelf.keys():
                return "Car not found"
            self.car = identifier
            self.location = self.shelf[identifier]["location"]
        #if parseable to integer it is taken as parking spot number
        else:
            if int(identifier)>=numberofSpots:
                return "Invalid location"
            elif identifier not in self.shelf.keys():
                return "Location was free"
            self.car = self.shelf[identifier]
            self.location = identifier 
        return ""
    
    
    