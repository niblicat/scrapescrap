from module_2.htmlparser import OnionParser
from abc import ABC, abstractmethod
from requests import Response
from essentials import colour
import requests

# * Goal: Use dependence inversion so components are abstracted
# * and can be swapped out easily

class PageDataRetriever(ABC):
    """
    Gives the page data as a string given a page URL string
    """
    @abstractmethod
    def GetPageDataFromURL(pageURL: str) -> str:
        raise NotImplementedError("Implemented by subclass")

class OnionPageDataRetriever(PageDataRetriever):
    """
    Gives the page data as a string given a page URL string
    """
    def GetPageDataFromURL(pageURL: str) -> str:
        """
        Retrieves the main page data from a URL
        """
        page: Response = requests.get(pageURL)
        
        return page.text

class InputFileProcessor(ABC):
    """
    Defines methods for retrieving data from an input file
    """
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
    
class Scraper(ABC):
    """
    Abstract method that defines what the web scraper should do
    """
    @abstractmethod
    def ScrapeFromFile(inputFile: str, baseOutput: str = "output") -> None:
        """
        Obtains URLS from a text inputFile and outputs JSON files pertaining to each webpage
        Outputs to files named {baseOutput}N where N is the URL index from the inputFile
        """
        raise NotImplementedError("Implemented by subclass")

class OnionScraper(Scraper):
    def ScrapeFromFile(inputFile: str = "input.txt", baseOutput: str = "output") -> None:
        urls = OnionInputFileProcessor.GetURLsFromText(inputFile)
        i = 0
        for url in urls:
            # output to the terminal which file is being processed
            print(colour.OKGREEN + "url:" + colour.ENDC, url)
            currentOutput = baseOutput + str(i)
            i += 1
            
            pageData = OnionPageDataRetriever(url)
            
            # send to parser so it can output the data
            OnionParser.ParseDataFromPage(pageData, currentOutput)