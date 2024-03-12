from essentials import colour, Slide, PageContent
from bs4 import BeautifulSoup
from bs4 import Tag

def ParseFirstSlide(section: Tag) -> Slide:
    """
    Parses a slide without a header, which is typically the first slide
    """
    contentDiv: Tag = section.contents[1]
    imageLink = contentDiv.img['src']
    # print(imageLink)
    content = contentDiv.p.getText()
    # print("content", content)
    return Slide(header="", image=imageLink, text=content)

def ParseSlide(section: Tag) -> Slide:
    """
    Parses a typically formatted slide
    """
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
    """
    Retrieves the main page data from a URL and retrieves significant information
    """
    # TODO: Move this to webscraper
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

def ScrapeFromURLToJSON(url: str, output: str = "output") -> None:
    """
    Takes a URL given in a string and outputs the relevant data to a file
    """
    page: PageContent = GetContentFromPage(url)
    pageStr = page.to_json_string()
    outputFile = output + ".json"
    with open(outputFile, 'w') as file:
        file.write(pageStr)

def ScrapeFromFile(inputFile: str = "input.txt", baseOutput: str = "output") -> None:
    """
    Obtains URLS from a text file and outputs JSON files pertaining to each webpage
    """
    urls = GetURLsFromText(inputFile)
    i = 0
    for url in urls:
        print(colour.OKGREEN + "url:" + colour.ENDC, url)
        currentOutput = baseOutput + str(i)
        i += 1
        ScrapeFromURLToJSON(url, currentOutput)
        
def ParseFirstSlide(section: Tag) -> Slide:
    """
    Parses a slide without a header, which is typically the first slide
    """
    contentDiv: Tag = section.contents[1]
    imageLink = contentDiv.img['src']
    # print(imageLink)
    content = contentDiv.p.getText()
    # print("content", content)
    return Slide(header="", image=imageLink, text=content)

def ParseSlide(section: Tag) -> Slide:
    """
    Parses a typically formatted slide
    """
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
    """
    Retrieves the main page data from a URL and retrieves significant information
    """
    
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

def ScrapeFromURLToJSON(url: str, output: str = "output") -> None:
    """
    Takes a URL given in a string and outputs the relevant data to a file
    """
    page: PageContent = GetContentFromPage(url)
    pageStr = page.to_json_string()
    outputFile = output + ".json"
    with open(outputFile, 'w') as file:
        file.write(pageStr)

def ScrapeFromFile(inputFile: str = "input.txt", baseOutput: str = "output") -> None:
    """
    Obtains URLS from a text file and outputs JSON files pertaining to each webpage
    """
    urls = GetURLsFromText(inputFile)
    i = 0
    for url in urls:
        print(colour.OKGREEN + "url:" + colour.ENDC, url)
        currentOutput = baseOutput + str(i)
        i += 1
        ScrapeFromURLToJSON(url, currentOutput)