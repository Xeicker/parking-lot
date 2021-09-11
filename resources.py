from flask_restful import Resource
from flask import request
from parking_lot import ParkingLotManager
from webargs.flaskparser import parser
from webargs import fields
import logging


class CarResource(Resource):
    # Needed argumetns for car addition an deletion
    _car_add_args = {"car": fields.Str(), "tariff": fields.Str()}
    _car_delete_args = {"car": fields.Str(), "location": fields.Integer()}

    # Logger to use for any logging functionality
    logger = logging.getLogger("CarList")

    # Status strings
    _success_string = "success"
    _fail_string = "fail"

    # Http response codes
    _succesful_listing_code = 200
    _bad_request_code = 400
    _succesful_car_addition_code = 201
    _succesful_car_deletion_code = 200

    def __init__(self):
        self.parking_lot_manager = ParkingLotManager()

    def _make_request_response(self, message, info, response_code):
        response = {
            "status": self._fail_string if message else self._success_string}
        # Message key only appears when any error occurs
        if message:
            response["message"] = message
            return response, response_code
        # Concat response with additional information needed
        response.update(info)
        return response, response_code

    # GET request
    def get(self):
        return self._make_request_response(
            "",
            {"cars": self.parking_lot_manager.get_all_cars()},
            self._succesful_listing_code)

    # POST request
    def post(self):

        # Read arguments from the body of the request and validate them
        args = parser.parse(self._car_add_args, request, location="json")
        message = self._validate_add_request_arguments(args)

        # If any error fail the request
        if message:
            self.logger.info("Bad request with args: " + str(args) +
                             "; \nError message: " + message)
            return self._make_request_response(
                message,
                None,
                self._bad_request_code)

        # Generate car info
        car = self._build_car(args)

        # Add car to db
        self.parking_lot_manager.add_car(car)

        return self._make_request_response(
            "",
            car.get_as_dict(),
            self._succesful_car_addition_code)

    # DELETE request
    def delete(self):

        args = parser.parse(self._car_delete_args, request, location="json")
        message, car = self._validate_delete_request_arguments(args)

        # Fail request if any error on identifier
        if message:
            return self._make_request_response(
                message,
                None,
                self._bad_request_code)

        # Delete car from db
        deletion_response = self.parking_lot_manager.delete_car(car)

        # Concat car info with request info
        response = {'status': 'success'}
        response.update(deletion_response)
        return self._make_request_response(
            "",
            deletion_response,
            self._succesful_car_deletion_code)

    def _validate_add_request_arguments(self, args):
        msg = []
        # Missing arguments test
        if "car" not in args:
            msg.append("missing car argument")
        if "tariff" not in args:
            msg.append("missing tariff argument")
        if msg:
            return " and ".join(msg).capitalize()

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

    def _validate_delete_request_arguments(self, args):
        # Missing arguments test
        if "car" not in args and "location" not in args:
            return ("missing car argument, request needs to" +
                    "contain either location or car argument"), None
        # if identifier is not parseable to integer then it is taken as car ID
        if "car" in args:
            identifier = args["car"]
            if identifier.isdigit():
                return "car argument must be non-integer", None
            car = self.parking_lot_manager.get_car_by_id(identifier)
            if car is None:
                return "car not found", None
        # if parseable to integer it is taken as parking spot number
        else:
            identifier = str(args["location"])
            car = self.parking_lot_manager.get_car_at_spot(identifier)
            if int(identifier) >= self.parking_lot_manager.parking_spots:
                return "Invalid location", None
            elif car is None:
                return "Location was free", None
        return "", car
