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
        return {'status': 'success', 'cars': [x for x in cars if isinstance(x,dict)]}, 200
    def post(self):
        self.shelf = get_db()
        args = parser.parse(self.car_add_args,request,location="json")
        message = self.validatePostRequestArguments(args)
        if message:
            return {"status": "fail", "message" : message} , 400
        car = self.buildCar(args)
        self.shelf[args["car"]] = car
        self.shelf[str(self.spot)] = args["car"]
        response = {'status': 'success'}
        response.update(car)
        return response, 201
    def validatePostRequestArguments(self,args):
        msg = []
        #Missing arguments test
        if "car" not in args:
            msg.append("missing car argument")
        if "tariff" not in args:
            msg.append("missing tariff argument")
        if msg:
            return " and ".join(msg).capitalize()
        print(msg)
        
        #Correct format arguments
        if len(args["car"])==0 or args["car"].isdigit():
            msg.append("car argument must be a non integer non empty string")
        if args["tariff"] not in tariffs:
            msg.append("tariff has to be one of: " + ",".join(tariffs))
        if msg:
            return " and ".join(msg).capitalize()
        
        #Validate unique car ids
        elif args["car"] in self.shelf.keys():
            return "This car id has already been registered"
        
        #Validate parking lot spot availability
        self.spot = self.getSpot()
        if self.spot<0:
            return "Parking lot is full"
        return ""
    def buildCar(self, args):
        return {
            "car": args["car"],
            "tariff": args["tariff"],
            "location": str(self.spot),
            "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    def getSpot(self):
        for i in range(1, numberofSpots+1):
            if str(i) not in self.shelf.keys():
                return i
        return -1
class Car(Resource):
    def delete(self,identifier):
        self.shelf = get_db()
        message = self.validateDeleteRequestArguments(identifier)
        if message:
            return {"status" : "fail","message" : message} , 400
        fromd = datetime.strptime(self.shelf[self.car]["start"],"%Y-%m-%d %H:%M:%S")
        tod = datetime.now()
        fee = calculateFee(fromd,tod,self.shelf[self.car]["tariff"])
        carobj = self.shelf[self.car]
        carobj["finish"] = tod.strftime("%Y-%m-%d %H:%M:%S")
        del self.shelf[self.car]
        del self.shelf[self.location]
        response = {'status': 'success',"fee":fee}
        response.update(carobj)
        return response,200
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
    
    
    