import pytest

from module_2.htmlparser import OnionParser

f = open('testpage.txt', 'r')
testpage = f.read()

defaultOutput = "output"

def test_no_env():
    with pytest.raises(FileNotFoundError):
        OnionParser.ParseDataFromPage(testpage, defaultOutput, True)