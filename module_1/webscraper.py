import requests
from requests import Response

def GetURLsFromText(file: str = "input.txt") -> list[str]:
    """
    Returns a list of URLS given a properly formatted input txt formatted file
    """
    with open(file) as text:
        urls = text.read().split()
    return urls

def GetPageDataFromURL(pageURL: str) -> Response:
    """
    Retrieves the main page data from a URL
    """
    page: Response = requests.get(pageURL)
    
    return page