import math

tariffs = {"hourly": lambda fromd, tod: basic_tariff(fromd, tod, 3600, 2),
           "daily": lambda fromd, tod: basic_tariff(fromd, tod, 3600*24, 30)}
number_of_spots = 10


def basic_tariff(fromd, tod, divisor, factor):
    return math.ceil((tod-fromd).total_seconds()/float(divisor))*factor


def calculate_fee(fromd, tod, tariff):
    # Any tariff is free first 15 minutes
    if (tod-fromd).total_seconds() <= 15*60:
        return 0

    elif tariff in tariffs:
        return tariffs[tariff](fromd, tod)
    raise Exception("Unknown tariff")
