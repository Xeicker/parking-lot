from ParkinLotManager import basicTariff, calculateFee
from datetime import datetime

# test basic tariff function


def test_basicTariff():
    # Test 10 exact minutes fee with 1 dollar per minute
    # (no 15 minutes free policy applied)
    assert basicTariff(datetime(2020, 9, 2, 5, 20),
                       datetime(2020, 9, 2, 5, 30), 60, 1) == 10
    # Test 1 hour and 10 minutes fee with 1 dollar per hour
    assert basicTariff(datetime(2020, 9, 2, 5, 20),
                       datetime(2020, 9, 2, 6, 30), 3600, 1) == 2
    # Test 1 day 1 hour and 10 minutes fee with 1 dollar per day
    assert basicTariff(datetime(2020, 9, 2, 5, 20),
                       datetime(2020, 9, 3, 6, 30), 24*3600, 1) == 2

# test calculate Fee function


def test_calculateFee():
    # Test free frist 15 minutes
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 2, 5, 30), "hourly") == 0
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 2, 5, 30), "daily") == 0
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 2, 5, 30), "monthly") == 0

    # Test hourly tariff
    # 24 exat hours
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 2, 6, 20), "hourly") == 24
    # A bit more than an hour
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 2, 6, 30), "hourly") == 4

    # Test daily tariff
    # A bit more than 24 hours
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 3, 6, 30), "daily") == 60
    # Exactly 24 hours
    assert calculateFee(datetime(2020, 9, 2, 5, 20),
                        datetime(2020, 9, 3, 5, 20), "daily") == 30
