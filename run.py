from bs4 import BeautifulSoup
from bs4 import Tag
import requests
import json
from argparse import ArgumentParser
import os
from dataclasses import dataclass

class colour:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class Slide():
    header: str
    image: str
    text: str

    def to_dict(self) -> dict:
        return {
            "header": self.header,
            "image": self.image,
            "text": self.text
        }

@dataclass
class PageContent():
    title: str
    slides: list[Slide]

    def to_json_string(self) -> str:
        dicts = [slide.to_dict() for slide in self.slides]
        return json.dumps({"title": self.title, "slides": dicts}, indent=2)

def GetURLsFromText(file: str = "input.txt") -> list[str]:
    with open(file) as text:
        urls = text.read().split()
    return urls

def ExtractText(raw: str) -> str:
    return raw[-1]

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

def GetContentFromPage(pageURL) -> PageContent:
    # get page data from URL
    page = requests.get(pageURL)
    # pass page text through beautiful soup
    bsPage = BeautifulSoup(page.text, 'html.parser')
    # print(bsPage.prettify())
    title = bsPage.h1.string
    # print("title", title)
    
    # Output depends on if article is slide-type or paragraph-type
    sections = bsPage.find_all('section')
    slideList: list[Slide] = []
    if (len(sections) <= 0):
        # print("length", len(sections), title, pageURL)
        article: Tag = bsPage.find_all('div', {'class': 'js_starterpost'})[0]
        newSlide = ParseFirstSlide(article)
    else:
        newSlide = ParseFirstSlide(sections[0])
    slideList.append(newSlide)

    for section in sections[1:-1]:
        newSlide = ParseSlide(section)
        slideList.append(newSlide)
    
    return PageContent(title=title, slides=slideList)

def ScrapeFromURLToJson(url: str, output: str = "output") -> None:
    page: PageContent = GetContentFromPage(url)
    pageStr = page.to_json_string()
    outputFile = output + ".json"
    with open(outputFile, 'w') as file:
        file.write(pageStr)

def ScrapeFromFile(inputFile: str = "input.txt", baseOutput: str = "output") -> None:
    urls = GetURLsFromText(inputFile)
    i = 0
    for url in urls:
        print(colour.OKGREEN + "url:" + colour.ENDC, url)
        currentOutput = baseOutput + str(i)
        i += 1
        ScrapeFromURLToJson(url, currentOutput)

    
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
    else:
        print(colour.FAIL + "Invalid file type. Please use a .txt file." + colour.ENDC)
        exit()
    
    print(colour.BOLD + "Scraping urls..." + colour.ENDC)
    ScrapeFromFile(inputPath, outputBase)

if __name__ == "__main__":
    main()