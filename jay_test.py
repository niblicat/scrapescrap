#file: jaytest.py 

import pytest
from requests import Response
from module_1 import webscraper

test_url = "https://www.theonion.com/quiz-are-you-a-sociopath-1851326704"

def test_Scraper():
    with pytest.raises(NotImplementedError):
        webscraper.Scraper.GetPageDataFromURL(test_url)

def test_OnionScraper():
    assert isinstance(webscraper.OnionScraper.GetPageDataFromURL(test_url), str)

def test_InputFileProcessor():
    with pytest.raises(NotImplementedError):
        webscraper.InputFileProcessor.GetURLsFromText(test_url)

def test_OnionInputFileProcessor():
    assert len(webscraper.OnionInputFileProcessor.GetURLsFromText("input.txt")) != 0