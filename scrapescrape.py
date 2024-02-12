from bs4 import BeautifulSoup
from bs4 import Tag
import requests
from dataclasses import dataclass

@dataclass
class Slide():
    header: str
    image: str
    text: str

@dataclass
class PageContent():
    title: str
    slides: list[Slide]

def ExtractText(raw: str) -> str:
    return raw[-1]

def ParseFirstSlide(section: Tag) -> Slide:
    contentDiv: Tag = section.contents[1]
    imageLink = contentDiv.img['src']
    # print(imageLink)
    content = contentDiv.p.getText()
    # print(content)
    return Slide(header="", image=imageLink, text=content)

def ParseSlide(section: Tag) -> Slide:
    headerDiv: Tag = section.contents[3]
    header = headerDiv.h2.getText()
    # print(header) # Slide head
    contentDiv: Tag = section.contents[4]
    imageLink = contentDiv.img['src']
    # print(imageLink)
    content = contentDiv.p.getText()
    # print(content)
    return Slide(header=header, image=imageLink, text=content)

def GetContentFromPage(pageURL) -> PageContent:
    # get page data from URL
    page = requests.get(pageURL)
    # pass page text through beautiful soup
    bsPage = BeautifulSoup(page.text, 'html.parser')
    # print(bsPage.prettify())
    title = bsPage.h1.string
    # print(title)
    
    slideList: list[Slide] = []
    sections = bsPage.find_all('section')
    newSlide = ParseFirstSlide(sections[0])
    slideList.append(newSlide)
    for section in sections[1:-1]:
        newSlide = ParseSlide(section)
        slideList.append(newSlide)
    
    return PageContent(title=title, slides=slideList)
    

def main():
    GetContentFromPage("https://www.theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755/slides/4")

if __name__ == "__main__":
    main()