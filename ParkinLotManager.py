import math

tariffs = {"hourly": lambda fromd,tod: basicTariff(fromd,tod,3600,2)
 , "daily": lambda fromd,tod: basicTariff(fromd,tod,3600*24,30)}
numberofSpots = 10
def basicTariff(fromd, tod, divisor,factor):
    return math.ceil((tod-fromd).total_seconds()/float(divisor))*factor
def calculateFee(fromd, tod, tariff):
    if (tod-fromd).total_seconds()<=15*60:
        return 0
    elif tariff in tariffs:
        return tariffs[tariff](fromd,tod)
    raise Exception("Unknown tariff")