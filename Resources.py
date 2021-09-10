from flask_restful import Resource
from flask import request
from ParkinLotManager import ParkingLotManager
from webargs.flaskparser import parser
from webargs import fields
import logging


class CarList(Resource):
    car_add_args = {"car": fields.Str(), "tariff": fields.Str()}
    logger = logging.getLogger("CarList")

    def __init__(self):
        self.parking_lot_manager = ParkingLotManager()

    # GET request
    def get(self):
        return {'status': 'success',
                'cars': self.parking_lot_manager.get_all_cars()}, 200

    # POST request
    def post(self):

        # Read arguments from the body of the request and validate them
        args = parser.parse(self.car_add_args, request, location="json")
        message = self._validate_add_request_arguments(args)

        # If any error fail the request
        if message:
            self.logger.info("Bad request with args: " + str(args) +
                             "; \nError message: " + message)
            return {"status": "fail", "message": message}, 400

        # Generate car info
        car = self._build_car(args)

        # Add car to db
        self.parking_lot_manager.add_car(car)

        # Concat status info to car info
        response = {'status': 'success'}
        response.update(car.get_as_dict())
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
        if args["tariff"] not in self.parking_lot_manager.tariffs:
            msg.append("tariff has to be one of: " +
                       ",".join(self.parking_lot_manager.tariffs))
        if msg:
            return " and ".join(msg).capitalize()

        # Validate unique car ids
        car = self.parking_lot_manager.get_car_by_id(args["car"])
        if car is not None:
            return "This car id has already been registered"

        # Validate parking lot spot availability
        self.spot = self.parking_lot_manager.get_spot()
        if self.spot < 0:
            return "Parking lot is full"
        return ""

    def _build_car(self, args):
        return self.parking_lot_manager.generate_new_car(
            args["car"], args["tariff"])


class CarResource(Resource):
    def __init__(self):
        self.parking_lot_manager = ParkingLotManager()

    # DELETE request
    def delete(self, identifier):
        message, car = self._validate_delete_request_arguments(identifier)

        # Fail request if any error on identifier
        if message:
            return {"status": "fail", "message": message}, 400

        # Delete car from db
        deletion_response = self.parking_lot_manager.delete_car(car)

        # Concat car info with request info
        response = {'status': 'success'}
        response.update(deletion_response)
        return response, 200

    def _validate_delete_request_arguments(self, identifier):
        if len(identifier) == 0:
            return "Missing identifier", None
        # if identifier is not parseable to integer then it is taken as car ID
        elif not identifier.isdigit():
            car = self.parking_lot_manager.get_car_by_id(identifier)
            if car is None:
                return "Car not found", None
        # if parseable to integer it is taken as parking spot number
        else:
            car = self.parking_lot_manager.get_car_at_spot(identifier)
            if int(identifier) >= self.parking_lot_manager.parking_spots:
                return "Invalid location", None
            elif car is None:
                return "Location was free", None
        return "", car
