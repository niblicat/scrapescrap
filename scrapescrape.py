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

def ScrapeFromFileToText(file: str = "input.txt") -> None:
#     urls = ["https://www.theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755",
# "https://www.theonion.com/follow-taylor-swift-s-every-move-with-our-real-time-jet-1851240542",
# "https://www.theonion.com/signs-you-are-a-beta-male-1851221877",
# "https://www.theonion.com/fans-speculate-whether-taylor-swift-will-make-it-to-sup-1851243533",
# "https://www.theonion.com/another-field-goal-blocked-by-cirque-du-soleil-performe-1851243517"]
#     for url in urls:
#         print("url", url)
#         GetContentFromPage(url)
    urls = GetURLsFromText(file)
    for url in urls:
        print("url", url)
        GetContentFromPage(url)
def main() -> None:
    # GetContentFromPage("https://www.theonion.com/pros-and-cons-of-shutting-down-the-border-1851235755")
    # GetContentFromPage("https://www.theonion.com/follow-taylor-swift-s-every-move-with-our-real-time-jet-1851240542")
    # GetContentFromPage("https://www.theonion.com/signs-you-are-a-beta-male-1851221877")
    # GetContentFromPage("https://www.theonion.com/fans-speculate-whether-taylor-swift-will-make-it-to-sup-1851243533")
    # GetContentFromPage("https://www.theonion.com/another-field-goal-blocked-by-cirque-du-soleil-performe-1851243517")
    # print(GetURLsFromText("input.txt"))
    ScrapeFromFileToText("input.txt")

if __name__ == "__main__":
    main()