from flask_restful import Resource
from Shelves import get_db
from flask import request
from ParkinLotManager import tariffs, number_of_spots, calculate_fee
from webargs.flaskparser import parser
from webargs import fields
from datetime import datetime


class CarList(Resource):
    car_add_args = {"car": fields.Str(), "tariff": fields.Str()}

    # GET request
    def get(self):
        shelf = get_db()
        cars = []

        # Read all items from db
        for key in shelf.keys():
            cars.append(shelf[key])

        # return list of all items in db which are cars
        return {'status': 'success', 'cars':
                [x for x in cars if isinstance(x, dict)]}, 200

    # POST request
    def post(self):
        self.shelf = get_db()

        # Read arguments from the body of the request and validate them
        args = parser.parse(self.car_add_args, request, location="json")
        message = self.validate_add_request_arguments(args)

        # If any error fail the request
        if message:
            return {"status": "fail", "message": message}, 400

        # Generate car info
        car = self.build_car(args)

        # Save car to db
        self.shelf[args["car"]] = car

        # Associate parking spot to carId
        self.shelf[str(self.spot)] = args["car"]

        # Concat status info to car info
        response = {'status': 'success'}
        response.update(car)
        return response, 201

    def _validate_add_request_arguments(self, args):
        msg = []
        # Missing arguments test
        if "car" not in args:
            msg.append("missing car argument")
        if "tariff" not in args:
            msg.append("missing tariff argument")
        if msg:
            return " and ".join(msg).capitalize()
        print(msg)

        # Correct format arguments
        if len(args["car"]) == 0 or args["car"].isdigit():
            msg.append("car argument must be a non integer non empty string")
        if args["tariff"] not in tariffs:
            msg.append("tariff has to be one of: " + ",".join(tariffs))
        if msg:
            return " and ".join(msg).capitalize()

        # Validate unique car ids
        elif args["car"] in self.shelf.keys():
            return "This car id has already been registered"

        # Validate parking lot spot availability
        self.spot = self.get_spot()
        if self.spot < 0:
            return "Parking lot is full"
        return ""

    def _build_car(self, args):
        return {
            "car": args["car"],
            "tariff": args["tariff"],
            "location": str(self.spot),
            "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _get_spot(self):
        # Find first available parking spot
        for i in range(1, number_of_spots+1):
            if str(i) not in self.shelf.keys():
                return i
        return -1


class Car(Resource):
    # DELETE request
    def delete(self, identifier):
        self.shelf = get_db()
        message = self.validate_delete_request_arguments(identifier)

        # Fail request if any error on identifier
        if message:
            return {"status": "fail", "message": message}, 400

        # Generate info to calculate fee and calculate it
        carobj = self.shelf[self.car]
        fromd = datetime.strptime(carobj["start"], "%Y-%m-%d %H:%M:%S")
        tod = datetime.now()
        fee = calculate_fee(fromd, tod, carobj["tariff"])

        # Extend car info
        carobj["finish"] = tod.strftime("%Y-%m-%d %H:%M:%S")

        # Delete car from db
        del self.shelf[self.car]
        del self.shelf[self.location]

        # Concat car info with request info
        response = {'status': 'success', "fee": fee}
        response.update(carobj)
        return response, 200

    def _validate_delete_request_arguments(self, identifier):
        if len(identifier) == 0:
            return "Missing identifier"
        # if identifier is not parseable to integer then it is taken as car ID
        elif not identifier.isdigit():
            if identifier not in self.shelf.keys():
                return "Car not found"
            self.car = identifier
            self.location = self.shelf[identifier]["location"]
        # if parseable to integer it is taken as parking spot number
        else:
            if int(identifier) >= number_of_spots:
                return "Invalid location"
            elif identifier not in self.shelf.keys():
                return "Location was free"
            self.car = self.shelf[identifier]
            self.location = identifier
        return ""
