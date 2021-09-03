from ParkinLotManager import basicTariff, calculateFee
from datetime import datetime

def test_basicTariff():
    assert basicTariff(datetime(2020,9,2,5,20),datetime(2020,9,2,5,30),60,1)==10
    assert basicTariff(datetime(2020,9,2,5,20),datetime(2020,9,2,6,30),3600,1)==2
    assert basicTariff(datetime(2020,9,2,5,20),datetime(2020,9,3,6,30),24*3600,1)==2
def test_calculateFee():
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,2,5,30),"hourly")==0
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,2,5,30),"daily")==0
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,2,5,30),"monthly")==0
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,2,6,20),"hourly")==2
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,2,6,30),"hourly")==4
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,3,6,30),"daily")==60
    assert calculateFee(datetime(2020,9,2,5,20),datetime(2020,9,3,5,20),"daily")==30
    