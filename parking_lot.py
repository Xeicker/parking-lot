from datetime import datetime
import math
import configparser
from shelves import Shelves, Car


class ParkingLotManager():
    tariffs = {}
    parking_spots = -1

    def __init__(self, testing=False):
        self.parser = configparser.ConfigParser(allow_no_value=True)
        self._load_configurations()
        if not testing:
            self.shelf = Shelves.get_db()

    def _basic_tariff(self, fromd, tod, divisor, factor):
        """Calculates a fee depending on time (seconds/divisor)
        multiplied by a cost per unit time(factor)"""
        print(divisor, factor, fromd, tod)
        return math.ceil((tod-fromd).total_seconds()
                         / float(divisor))*float(factor)

    def _load_configurations(self):
        self.parser.read("parkinglot.ini")
        for tariff_type in self.parser["Tariff_Types"]:
            if tariff_type == "basic_tariffs":
                # Tariffs based on basic_tariff function
                for tariff in self.parser[tariff_type]:
                    tariff_details = \
                        self.parser[tariff]
                    seconds = tariff_details["seconds"]
                    cost = tariff_details["cost"]
                    self.tariffs[tariff] = lambda \
                        fromd,\
                        tod,\
                        divisor = seconds,\
                        factor = cost:\
                        self._basic_tariff(fromd,
                                           tod,
                                           divisor,
                                           factor)
        # Load number of available spots in parking lot
        self.parking_spots = \
            int(self.parser["General_Config"]["parking_spots"])

    def calculate_fee(self, fromd, tod, tariff):
        """Calculates parking fee based on tariff and
        time(since 'fromd' to 'tod')"""
        # Any tariff is free first 15 minutes
        if (tod-fromd).total_seconds() <= 15*60:
            return 0

        elif tariff in self.tariffs:
            return self.tariffs[tariff](fromd, tod)
        raise Exception("Unknown tariff")

    def get_spot(self):
        """Finds first available parking spot and returns it
        if it is full returns -1"""
        for i in range(1, self.parking_spots+1):
            if str(i) not in self.shelf.keys():
                return i
        return -1

    def add_car(self, car):
        # Save car to Db through shelf dictionary
        self.shelf[car.id] = car
        self.shelf[str(car.location)] = car.id

    def get_all_cars(self):
        cars = []
        # Read items from Db
        for key in self.shelf.keys():
            cars.append(self.shelf[key])
        # Return the Car instances as dictionaries
        return [car.get_as_dict() for car in cars if isinstance(car, Car)]

    def get_car_at_spot(self, location):
        # Db relates each location to a carId
        if location in self.shelf.keys():
            return self.shelf[self.shelf[location]]
        return None

    def get_car_by_id(self, id):
        if id in self.shelf.keys():
            return self.shelf[id]
        return None

    def delete_car(self, car):
        """Deletes a car from the parking lot db, calculates fee
        and returns a response with car deleted and fee"""
        # Define the time at remotion
        car.finish = datetime.now()

        fee = self.calculate_fee(car.start, car.finish, car.tariff)

        # Concat fee value with car
        response = {"fee": fee}
        response.update(car.get_as_dict())

        # Delete car from Db
        del self.shelf[str(car.location)]
        del self.shelf[car.id]

        return response

    def generate_new_car(self, id, tariff):
        """Generates a car object with given id and tariff.
        if spot is available it is assigned to the car and
        date and time of addition"""
        spot = self.get_spot()
        # Parking lot is full
        if(spot < 0):
            return None
        return Car(id, tariff, spot, datetime.now())
