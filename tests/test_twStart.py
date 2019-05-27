import pytest
import sys
sys.path.append("../")
from src import twStart as twLib
from datetime import datetime

@pytest.mark.parametrize('testData, shouldBe', 
        [("Sat Aug 19 12:51:00 +0000 2019", "20190819"), 
         ("Fri Jul 30 12:51:00 +0000 1976", "19760730")])
def test_TwitterDateAsString(testData, shouldBe):
    result = twLib.FormatTwitterDate(testData, 'S')
    assert result == shouldBe, "Date format as string is not working properly."

def test_TwitterDateAsDate():
    twDate = "Fri Jul 30 12:51:00 +0000 1976"
    shouldBe = datetime.strptime("19760730", '%Y%m%d')
    result = twLib.FormatTwitterDate(twDate, 'D')
    assert result == shouldBe, "Date format for date type is not working properly."

def test_authorIsInWhiteList():
    assert '114742002' in twLib.WHITE_LIST_USERS, "@mirmirik is not in WhiteList"

def test_TwitterIsOnline():
    assert twLib.check_internet(), "Cannot access to Twitter API"

def test_arraySplit_for_102_10():
        modulus, loop = twLib.splitArray(102, 10)
        assert modulus == 2, "Modulus is not correctly set"
        assert loop == 10, "Loop count is not correctly set"

def test_arraySplit_for_17_4():
        modulus, loop = twLib.splitArray(17, 4)
        assert modulus == 1, "Modulus is not correctly set"
        assert loop == 4, "Loop count is not correctly set"