from argparse import ArgumentParser
import os
from abc import ABC, abstractmethod

from essentials import colour
from module_1.webscraper import Scraper, OnionScraper, InputFileProcessor, OnionInputFileProcessor
from module_2.htmlparser import Parser, OnionParser

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
    
class OnionScrapeToParse(ScrapeToParse):
    def __init__(self, scraper: Scraper, parser: Parser, fileProcessor: InputFileProcessor):
        self.scraper: Scraper = scraper
        self.parser: Parser = parser
        self.processor: InputFileProcessor = fileProcessor

    def Process(self, inputFile: str, outputSignature: str) -> None:
        urls = self.processor.GetURLsFromText(inputFile)
        for i, url in enumerate(urls):
            # output to the terminal which file is being processed
            print(colour.OKGREEN + "url:" + colour.ENDC, url)
            currentOutput = outputSignature + str(i)
            
            pageData = self.scraper.GetPageDataFromURL(url)
            
            # send to parser so it can output the data
            self.parser.ParseDataFromPage(pageData, currentOutput)

def main() -> None: 
    parser = ArgumentParser()
    parser.add_argument(help="Input text file", dest="input_path", type=str)
    parser.add_argument("--output", help="Output file base name (no extension)", dest="output_base", type=str, default="output")
    args = parser.parse_args()
    inputPath = args.input_path
    outputBase = args.output_base

    inputType = os.path.splitext(inputPath)[-1].lower()
    if (inputType == ""):
        inputPath += ".txt"
        print(colour.WARNING + "Normalising input by adding .txt extension..." + colour.ENDC)
    elif (inputType != ".txt"):
        print(colour.FAIL + "Invalid file type. Please use a .txt file." + colour.ENDC)
        exit()
    
    scrapeToParse = OnionScrapeToParse(OnionScraper, OnionParser, OnionInputFileProcessor)
    print(colour.BOLD + "Scraping urls..." + colour.ENDC)
    scrapeToParse.Process(inputPath, outputBase)
    print(colour.BOLD + colour.OKCYAN + "Success!" + colour.ENDC)

if __name__ == "__main__":
    main()