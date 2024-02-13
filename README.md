# The Onion Article Web Scraper
Scrape multiple URLs provided in a text file which each output as a JSON file.

## How to use
Install [Conda](https://docs.conda.io/en/latest/)
Instal [Git CLI](https://cli.github.com/)

Clone this repository onto your local machine
```
git clone https://github.com/niblicat/scrapescrape.git
```

Navigate to the scraper directory (contains 'scraper.py' and 'environment.yml') in the terminal and type the following to copy the Python enviroment:
```
conda create -n environment.yml
```

To activate the environment, enter
```
conda activate scrapescrape
```

You now are ready to use the scraper.

## Usage
To run the scraper on some input file 'input.txt', use the following command
```
python onionscrape.py input.txt
```

To change the default JSON output file name, use the argument '--output'
For example,
```
python onionscrape.py input.txt --output funny
```
will output funny0.json, funny1.json, ... , funnyN.json given an input.txt fiel containing N urls

## Limitations
Will not work on pages featuring only an image with no paraggraph content