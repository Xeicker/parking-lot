import math
import configparser


class ParkingLotManager():
    tariffs = {}
    parking_spots = -1

    def __init__(self):
        self.parser = configparser.ConfigParser(allow_no_value=True)
        self._load_configurations()

    def _basic_tariff(self, fromd, tod, divisor, factor):
        return math.ceil((tod-fromd).total_seconds()/float(divisor))*factor

    def _load_configurations(self):
        self.parser.read("parkinglot.ini")
        for tariff_type in self.parser["Tariff_Types"]:
            if tariff_type == "basic_tariffs":
                for tariff in self.parser[tariff_type]:
                    tariff_details = \
                        self.parser[tariff]
                    self.tariffs[tariff] = lambda fromd, tod:\
                        self._basic_tariff(fromd,
                                           tod,
                                           tariff_details["seconds"],
                                           tariff_details["cost"])
        self.parking_spots = \
            int(self.parser["General_Config"]["parking_spots"])

    def calculate_fee(self, fromd, tod, tariff):
        # Any tariff is free first 15 minutes
        if (tod-fromd).total_seconds() <= 15*60:
            return 0

        elif tariff in self.tariffs:
            return self.tariffs[tariff](fromd, tod)
        raise Exception("Unknown tariff")
