from parking_lot import ParkingLotManager
from datetime import datetime
import configparser

# test basic tariff function


def test_basic_tariff():

    parking_lot_manager = ParkingLotManager(testing=True)
    # Test 10 exact minutes fee with 1 dollar per minute
    # (no 15 minutes free policy applied)
    assert parking_lot_manager._basic_tariff(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 2, 5, 30), 60, 1) == 10
    # Test 1 hour and 10 minutes fee with 1 dollar per hour
    assert parking_lot_manager._basic_tariff(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 2, 6, 30), 3600, 1) == 2
    # Test 1 day 1 hour and 10 minutes fee with 1 dollar per day
    assert parking_lot_manager._basic_tariff(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 3, 6, 30), 24*3600, 1) == 2

# test calculate Fee function


def test_calculate_fee():
    parking_lot_manager = ParkingLotManager(testing=True)

    # Test free frist 15 minutes
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 2, 5, 30), "hourly") == 0
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 2, 5, 30), "daily") == 0
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 2, 5, 30), "monthly") == 0

    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read("parkinglot.ini")

    hourlyfee = float(parser["hourly"]["cost"])
    dailyfee = float(parser["daily"]["cost"])

    # Test correct configuration of daily and hourly
    # tariffs seconds configuration
    assert parser["hourly"]["seconds"] == "3600"
    assert parser["daily"]["seconds"] == "86400"

    # Test hourly tariff
    # 24 exat hours
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 3, 5, 20), "hourly") == 24*hourlyfee
    # A bit more than an hour
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 2, 6, 30), "hourly") == 2*hourlyfee

    # Test daily tariff
    # A bit more than 24 hours
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 3, 6, 30), "daily") == 2*dailyfee
    # Exactly 24 hours
    assert parking_lot_manager.calculate_fee(
        datetime(2020, 9, 2, 5, 20),
        datetime(2020, 9, 3, 5, 20), "daily") == dailyfee
