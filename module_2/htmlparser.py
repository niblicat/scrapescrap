# Handles the parsing of an html file and outputs it to the raw and processed directory

from essentials import Slide, PageContent
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from bs4 import Tag

# * Goal: Use dependence inversion so components are abstracted
# * and can be swapped out easily

class SlideParser(ABC):
    """
    Abstract class that defines the methods needed to parse a single slide
    """
    @staticmethod
    @abstractmethod
    def ParseFirstSlide(section: Tag) -> Slide:
        """
        Parses a slide without a header, which is typically the first slide
        """
        raise NotImplementedError("Implemented by subclass")
    @staticmethod
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
        # TODO: Special case that may change in the future, may fix
        if (header == "You’ve Made It This Far..."):
            return None

        contentDiv: Tag = section.contents[4]
        # print(contentDiv)
        imageLink = contentDiv.img['src']
        # print(imageLink)
        content = ""
        if contentDiv.p is not None:
            content = contentDiv.p.getText()
            # print("content", content)

        return Slide(header=header, image=imageLink, text=content)

class PageParser(ABC):
    """
    Abstract class that defines the methods needed to parse an Onion webpage
    """
    @staticmethod
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
            if (type(newSlide) == Slide):
                slideList.append(newSlide)
        
        return PageContent(title=title, slides=slideList)

class OutputPage(ABC):
    """
    Abstract base class that uses outputs PageContent to a JSON-formatted file
    """
    @staticmethod
    @abstractmethod
    def PageContentToFile(pg: PageContent, output: str = "output"):
        """
        Accepts a PageContent object and outputs its data to a file
        """
        raise NotImplementedError("Implemented by subclass")
    @staticmethod
    @abstractmethod
    def StringToTXTFile(string: str, output: str = "output"):
        """
        Outputs a string to a txt file
        """
        raise NotImplementedError("Implemented by subclass")

class OnionOutputPage(OutputPage):
    def PageContentToFile(pg: PageContent, output: str = "output") -> None:
        pageStr = pg.to_json_string()
        outputFile = output + ".json"
        with open(outputFile, 'w') as file:
            file.write(pageStr)

    def StringToTXTFile(string: str, output: str = "output") -> None:
        outputFile = output + ".txt"
        with open(outputFile, 'w') as file:
            file.write(string)


class Parser(ABC):
    """
    Abstract base class that parses page data and outputs it
    """
    @staticmethod
    @abstractmethod
    def ParseDataFromPage(page: str, output: str):
        """
        Uses page HTML as a string to create an output
        """
        raise NotImplementedError("Implemented by subclass")

class OnionParser(Parser):
    def ParseDataFromPage(page: str, output: str, createSummary: bool = False) -> None:
        dest0 = "Data/raw/" + output
        dest1 = "Data/processed/" + output
        dest2 = "Data/summary/" + output
        
        # dump raw data before parsing
        OnionOutputPage.StringToTXTFile(page, dest0)
        pc: PageContent = OnionPageParser.ParsePageContent(page)
        OnionOutputPage.PageContentToFile(pc, dest1)
        if (createSummary):
            from module_3.generatedsummaries import OpenAIRequest
            # get a summary and place it in the summary directory
            pageText = pc.__str__()
            summary = OpenAIRequest.GenerateSummary(pageText)
            summaryOutput = pc.title + "\n" + summary # add title to output txt
            OnionOutputPage.StringToTXTFile(summaryOutput, dest2)