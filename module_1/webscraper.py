# Reads from a text file containing URLs and grabs the HTML content from those URLs

from module_2.htmlparser import OnionParser
from abc import ABC, abstractmethod
from requests import Response
import requests

# * Goal: Use dependence inversion so components are abstracted
# * and can be swapped out easily

class Scraper(ABC):
    """
    Gives the page data as a string given a page URL string
    """
    @staticmethod
    @abstractmethod
    def GetPageDataFromURL(pageURL: str) -> str:
        raise NotImplementedError("Implemented by subclass")

class OnionScraper(Scraper):
    """
    Gives the page data as a string given a page URL string
    """
    def GetPageDataFromURL(pageURL: str) -> str:
        """
        Retrieves the main page data from a URL
        """
        if "https://" in pageURL:
            page: Response = requests.get(pageURL)
        else:
            page: Response = requests.get("https://" + pageURL.strip())
        
        return page.text

class InputFileProcessor(ABC):
    """
    Defines methods for retrieving data from an input file
    """
    @staticmethod
    @abstractmethod
    def GetURLsFromText(file: str = "input.txt") -> list[str]:
        raise NotImplementedError("Implemented by subclass")

class OnionInputFileProcessor(InputFileProcessor):
    """
    Defines methods for retrieving data from an input file
    """
    def GetURLsFromText(file: str = "input.txt") -> list[str]:
        """
        Returns a list of URLS given a properly formatted input txt formatted file
        """
        with open(file) as text:
            urls = text.read().split()
        return urls