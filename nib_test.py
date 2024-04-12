import pytest
import os

from module_2.htmlparser import OnionParser
from module_1.webscraper import OnionScraper

useAPI = False

f = open('testpage.txt', 'r')
testpage = f.read()

defaultOutput = "output"

def test_backslash_output():
    OnionParser.ParseDataFromPage(testpage, '\\', False)
    assert os.path.exists("Data/processed/\\.json"), "File was not created"
    if useAPI:
        OnionParser.ParseDataFromPage(testpage, '\\', True)
        assert os.path.exists('Data/processed/\\.json'), "File was not created"

def test_perfect_url():
    assert OnionScraper.GetPageDataFromURL("https://www.theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755") is not None
    
def test_malformed_url():
    assert OnionScraper.GetPageDataFromURL("www.theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755") is not None
    assert OnionScraper.GetPageDataFromURL("theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755") is not None
    assert OnionScraper.GetPageDataFromURL("https://theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755") is not None
    
def test_bad_url():
    with pytest.raises(Exception):
        OnionScraper.GetPageDataFromURL("https://www.minecraft.fakeurl")