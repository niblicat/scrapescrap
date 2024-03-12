

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
class Slide:
    """
    Contains the basic data for a slide
    """
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
    """
    Holds the content for a webpage
    Contains a title and list of slides
    """
    title: str
    slides: list[Slide]

    def to_json_string(self) -> str:
        dicts = [slide.to_dict() for slide in self.slides]
        return json.dumps({"title": self.title, "slides": dicts}, indent=2)