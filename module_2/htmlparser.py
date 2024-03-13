from essentials import colour, Slide, PageContent
from bs4 import BeautifulSoup
from bs4 import Tag
from abc import ABC, abstractmethod

from module_1.webscraper import GetPageDataFromURL, GetURLsFromText

# * Goal: Use dependence inversion so components are abstracted
# * and can be swapped out easily

class SlideParser(ABC):
    """
    Abstract class that defines the methods needed to parse a single slide
    """
    @abstractmethod
    def ParseFirstSlide(section: Tag) -> Slide:
        """
        Parses a slide without a header, which is typically the first slide
        """
        raise NotImplementedError("Implemented by subclass")
    @abstractmethod
    def ParseSlide(section: Tag) -> Slide:
        """
        Parses a typically formatted slide
        """
        raise NotImplementedError("Implemented by subclass")
    
class OnionSlideParser(SlideParser):
    def ParseFirstSlide(section: Tag) -> Slide:
        contentDiv: Tag = section.contents[1]
        imageLink = contentDiv.img['src']
        # print(imageLink)
        content = contentDiv.p.getText()
        # print("content", content)
        return Slide(header="", image=imageLink, text=content)

    def ParseSlide(section: Tag) -> Slide:
        headerDiv: Tag = section.contents[3]
        header = headerDiv.h2.getText()
        # print(header) # Slide head
        contentDiv: Tag = section.contents[4]
        imageLink = contentDiv.img['src']
        # print(imageLink)
        content = contentDiv.p.getText()
        # print("content", content)
        return Slide(header=header, image=imageLink, text=content)

class PageParser(ABC):
    """
    Abstract class that defines the methods needed to parse an Onion webpage
    """
    @abstractmethod
    def ParsePageContent(unformattedPageContent: str) -> PageContent:
        raise NotImplementedError("Implemented by subclass")
    
class OnionPageParser(PageParser):
    def ParsePageContent(unformattedPageContent: str) -> PageContent:
        bsPage = BeautifulSoup(unformattedPageContent, 'html.parser')
        # print(bsPage.prettify())
        title = bsPage.h1.string
        # print("title", title)
        
        # Output depends on if article is slide-type or paragraph-type
        # Following block ensures we obtain the correct content with no errors
        sections = bsPage.find_all('section')
        slideList: list[Slide] = []
        if (len(sections) <= 0):
            # print("length", len(sections), title, pageURL)
            article: Tag = bsPage.find_all('div', {'class': 'js_starterpost'})[0]
            newSlide = OnionSlideParser.ParseFirstSlide(article)
        else:
            newSlide = OnionSlideParser.ParseFirstSlide(sections[0])
        slideList.append(newSlide)

        for section in sections[1:-1]:
            newSlide = OnionSlideParser.ParseSlide(section)
            slideList.append(newSlide)
        
        return PageContent(title=title, slides=slideList)

class OutputJSON(ABC):
    """
    Abstract base class that uses outputs PageContent to a JSON-formatted file
    """
    @abstractmethod
    def ScrapeFromURLToJSON(pg: PageContent, output: str = "output") -> None:
        """
        Accepts a PageContent object and outputs its data to a file
        """
        raise NotImplementedError("Implemented by subclass")

class OnionOutputJSON(OutputJSON):
    def ScrapeFromURLToJSON(pg: PageContent, output: str = "output") -> None:
        # ! implement this elsewhere
        # page: PageContent = GetContentFromPage(url)
        pageStr = pg.to_json_string()
        outputFile = output + ".json"
        with open(outputFile, 'w') as file:
            file.write(pageStr)

def Scraper(ABC):
    @abstractmethod
    def ScrapeFromFile(inputFile: str, baseOutput: str = "output") -> None:
        """
        Obtains URLS from a text inputFile and outputs JSON files pertaining to each webpage
        Outputs to files named {baseOutput}N where N is the URL index from the inputFile
        """
        raise NotImplementedError("Implemented by subclass")

def OnionScraper(Scraper):
    def ScrapeFromFile(inputFile: str = "input.txt", baseOutput: str = "output") -> None:
        urls = GetURLsFromText(inputFile)
        i = 0
        for url in urls:
            print(colour.OKGREEN + "url:" + colour.ENDC, url)
            currentOutput = baseOutput + str(i)
            i += 1
            ScrapeFromURLToJSON(url, currentOutput)