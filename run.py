# Manages the high level scrape to parse class and parses the command line arguments

from argparse import ArgumentParser
import os
from abc import ABC, abstractmethod

from essentials import colour
from module_1.webscraper import Scraper, OnionScraper, InputFileProcessor, OnionInputFileProcessor
from module_2.htmlparser import Parser, OnionParser

# * Goal: Use dependence inversion so components are abstracted
# * and can be swapped out easily

class ScrapeToParse(ABC):
    """
    Abstract base class that scrapes Onion pages and outputs them
    """
    @abstractmethod
    def Process(self, inputFile: str, outputSignature: str):
        """
        Given a file containing references to Onion content,
        output the relevant information
        """
        raise NotImplementedError("Implemented by subclass")
    
class ScrapeToParseFromFile(ScrapeToParse):
    """
    Scrapes from a text file to a file
    """
    def __init__(self, scraper: Scraper, parser: Parser, fileProcessor: InputFileProcessor):
        self.scraper: Scraper = scraper
        self.parser: Parser = parser
        self.processor: InputFileProcessor = fileProcessor

    def Process(self, inputFile: str, outputSignature: str, doSummary: bool = False) -> None:
        urls = self.processor.GetURLsFromText(inputFile)
        for i, url in enumerate(urls):
            # output to the terminal which file is being processed
            print(colour.OKGREEN + "url:" + colour.ENDC, url)
            currentOutput = outputSignature + str(i)
            
            pageData = self.scraper.GetPageDataFromURL(url)
            
            # send to parser so it can output the data
            self.parser.ParseDataFromPage(pageData, currentOutput, doSummary)

class ScrapeToParseFromURL(ScrapeToParse):
    """
    Scrapes a single url to a file
    """
    def __init__(self, scraper: Scraper, parser: Parser):
        self.scraper: Scraper = scraper
        self.parser: Parser = parser
    
    def Process(self, url: str, outputSignature: str) -> None:
        # output to the terminal which file is being processed
        print(colour.OKGREEN + "url:" + colour.ENDC, url)
        
        pageData = self.scraper.GetPageDataFromURL(url)
        
        # send to parser so it can output the data
        self.parser.ParseDataFromPage(pageData, outputSignature)

def main() -> None: 
    parser = ArgumentParser()
    parser.add_argument(help="Input text file", dest="input_path", type=str)
    parser.add_argument("--output", "-o", help="Output file base name (no extension)", dest="output_base", type=str, default="output")
    parser.add_argument("--summary", "-s", help="Output LLM-powered summaries", dest="do_summaries", action="store_true")
    args = parser.parse_args()
    inputPath = args.input_path
    outputBase = args.output_base
    doSummaries = args.do_summaries

    inputType = os.path.splitext(inputPath)[-1].lower()
    if (inputType == ""):
        inputPath += ".txt"
        print(colour.WARNING + "Normalising input by adding .txt extension..." + colour.ENDC)
    elif (inputType != ".txt"):
        print(colour.FAIL + "Invalid file type. Please use a .txt file." + colour.ENDC)
        exit()
    
    scrapeToParse = ScrapeToParseFromFile(OnionScraper, OnionParser, OnionInputFileProcessor)
    print(colour.BOLD + "Scraping urls..." + colour.ENDC)
    scrapeToParse.Process(inputPath, outputBase, doSummaries)
    print(colour.BOLD + colour.OKCYAN + "Success!" + colour.ENDC)

if __name__ == "__main__":
    main()