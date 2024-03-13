from argparse import ArgumentParser
import os

from essentials import colour
from module_1.webscraper import OnionScraper, OnionPageDataRetriever
from module_2.htmlparser import OnionParser

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
    
    print(colour.BOLD + "Scraping urls..." + colour.ENDC)
    OnionScraper.ScrapeFromFile(inputPath, outputBase)
    print(colour.BOLD + colour.OKCYAN + "Success!" + colour.ENDC)

if __name__ == "__main__":
    main()