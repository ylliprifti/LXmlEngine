# Data Retrieval Web Engine

## Context
Multiple technologies are used as web parsers, web scrapers, spider and so forth. 
Comparative studies can be found in [literature](http://ir.kdu.ac.lk/handle/345/1051) that 
categorise based on methods and technologies. We took a different perspective and looked at __querability__ feature.
Our inspiration comes form [OXPath](https://github.com/oxpath/oxpath) where an extension of XPath is used to "query" and extract semi-structured data from the web.

## Objectives
Similarly to [OXPath](https://github.com/oxpath/oxpath), our objective is to create a tool for data retrieval from the web based on a "query" mechanism. 
We opted for using JSON constructs for our query definitions with augmented keywords, filters and actions. 

## Technology stack
The tool is written in Python3 and can be included in other python projects by installing it from the python package index 
using `pip3 install dr-web-engine` or integrating with the tools command line interface by running `python3 -m web_engine.runner`
The tool is build on top of several other packages which will be automatically installed. These are: 
+ Selenium
+ Geckodriver Autoinstaller
+ LXML
+ Python Interface 
+ ArgParse
+ XVFBWrapper

XVFB only works on Linux and if the parameter is True on a Windows or MacOX system you will get an error message. 

The Python Package page can be found [here](https://pypi.org/project/dr-web-engine/)

## Usage

To use the integrated CLI run `python3 -m web_engine.runner`. This will display the following help message: 

```bash

usage: runner.py [-h] [-q QUERY] [-e [ENGINE]] [-ht [HEIGHT]] [-wh [WIDTH]]
                 [-lat [LAT]] [-lon [LON]] [-img [IMG]] [-l [LOG]]
                 [-xvfb [XVFB]]

Web Scrap Engine for semi-structured web data retrieval using JSON query constructs

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        JSON query
  -e [ENGINE], --engine [ENGINE]
                        Engine: use [lxml] for parser engine (default),
                        [selenium] for action based web scraping
  -ht [HEIGHT], --height [HEIGHT]
                        specify the browser window height (default is 800,
                        only used with Selenium engine)
  -wh [WIDTH], --width [WIDTH]
                        specify the browser window width (default is 1280,
                        only used with Selenium engine)
  -lat [LAT], --lat [LAT]
                        Latitude (not specified by default)
  -lon [LON], --lon [LON]
                        Longitude (not specified by default)
  -img [IMG], --img [IMG]
                        Load images
  -l [LOG], --log [LOG]
                        Set flag to True to see verbose logging output
  -xvfb [XVFB], --xvfb [XVFB]
                        Set flag to False to see Firefox when using Selenium
                        engine
                        
```

There is only one required parameter: `-q Query`

For example, to run the web data retrieval with the following JSON query (supposedly file `test.json`):

```json
{
    "_doc":"https://www.google.com/search?q=Donald+Duck",
    "links":[{
        "_base_path": "//div[@id='search'][1]//div[@class='g']",
        "_follow": "//a[@id='pnnext'][1]/@href",
        "link": "//div[@class='rc']/div[@class='r']/a/@href",
        "title": "//h3/text()"
    }]
}
```

use the following command: `python3 -m web_engine.runner -q test.json`. The outcome will look like the following JSON result: 

```json5

{"links": [{"link": ["https://en.wikipedia.org/wiki/Donald_Duck"], 
           "title": ["Donald Duck - Wikipedia"]},
           {"link": ["https://cosleyzoo.org/white-pekin-duck/"],
            "title": ["White Pekin Duck – Cosley Zoo"]},
           {"link": ["https://www.cheatsheet.com/entertainment/donald-duck-turned-85-years-old.html/"],
            "title": ["Donald Duck Turned 85-Years-Old and Disney Fans Are Quacking ..."]},
           {"link": ["https://en.wikipedia.org/wiki/Daisy_Duck"],
            "title": ["Daisy Duck - Wikipedia"]},
           {"link": ["https://www.headstuff.org/culture/history/disney-studios-war-story-donald-duck-became-sgt/"],
            "title": ["Disney Studios At War - the story of how Donald Duck became a Sgt ..."]}

```

In the JSON query provided, the items starting with `_` are keywords and can be filters, actions or instructions. 
If we remove all the keywords the remaining JSON represents the structure of the expected output. 

In another more complex query we use some other keywords and actions: 

```json

{
    "_doc": "https://www.checkatrade.com/trades/WayreHouseElectricalServices",
    "data": {
        "ld_data": "//head/script[@type=\"application/ld+json\"][1]"
    },
    "reviews": [{
            "_doc": "https://www.checkatrade.com/trades/WayreHouseElectricalServices/reviews",
            "_base_path": "//div[contains(@class, 'ReviewsPage__Content')]//div[contains(@class, 'ReviewsItem__Wrapper')]",
            "_key": "review",
            "_pre_remove": "//*[contains(@class,'alert-box')]",
            "_follow": "//a[contains(@class,\"Chevrons__Wrapper\")][2]/@href",
            "_follow_action": "//a[contains(@class,\"Chevrons__Wrapper\")][2]{click }",
            "title": "//h3[contains(@class, 'ReviewsItem__Title')]",
            "score": "//*[name()='svg']//text()[normalize-space()]",
            "verified": "//div[contains(@class, 'ReviewsItem__Verified')]/text()[normalize-space()]",
            "content": "//p[contains(@class, 'ReviewsItem__P')]",
            "review_by": "//div[contains(@class, 'ReviewsItem__Byline')]/text()[normalize-space()]"
        }]
}

```


## Keywords

`_doc`: Represents the document to follow. Is usually a URL to a web page.  It is compulsory on the top level and can be provided on the lower levels of the hierarchical structure. The `_doc` keyword  

`_base_path`: To be used in an array extraction. Arrays are a lists of element and are defined in the query as an JSON array `[]`. 
              When `_base_path` is provided, all elements of the query in the array will be looked inside the HTML element as defined by `_base_path`.   
              
`_key`: Use to assign each element of the array to assigned to the variable `_key`  

`_pre_xxx`: All actions that start with `_pre_` are to be executed before data extraction.  

`_pre_remove`: Remove elements from page  

`_follow`: Follow the link if and when exists  

`_follow_action`: If element in follow exists, then perform action rather than following the link. The actions are defined as the last part of the XPath query and are always defined between carley brackets. In this case the action `{click }` means click on element.  

## Extendability

The package is intended to be easily extendable. For example the `{click }` action is defined in the query as follows: 

The corresponding is defined as follows: 

```python
class ClickAction(implements(Action)):

    def __init__(self, receiver, log: logging = None):
        self._log = log
        self._receiver = receiver

    def execute(self, *args):
        if args is None or len(args) != 1:
            return
        xpath_selector: str = args[0]
        wait = WebDriverWait(self._receiver.driver, 10)
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_selector)))
        elem.click()
```

In the Scraper implementations, actions are registered against keywords as follows: 

```python

     click = ClickAction(self, self.log)
     filter_remove = FilterRemoveAction(self, self.log)
     self.register('click', click)
     self.register('remove', filter_remove)

```

And invoked by simply matching the action keywords in the query as follows: 

```python

    def action_get(self, actions: list):
        for x in actions:
            self.execute(x)
        return self.get()

    
    def execute(self, action_composite: str):
        action_name, action_path = SeleniumScraper.__get_action(action_composite)
        action_name = action_name.strip()
        if action_name in self._actions.keys():
            self._history.append((time.time(), action_name))
            self._actions[action_name].execute(action_path)
        else:
            self.log.warn(f"Command [{action_name}] not recognised")


    @staticmethod
    def __get_action(action_composite):
        pattern = '{(.+?)}'
        matches = re.search(pattern, action_composite)
        if not matches:
            return None, None
        action_name = matches.group(1)
        action_xpath = re.sub(pattern, '', action_composite)
        return action_name, action_xpath

```

## Future work

This work, whilst it is a working beta, is by no means complete and it's rather focused on a narrow specific problem. However, special effort has been made to keep the solution generic, universal and extendable for it to potentially grow into a mature Data Retrieval Web Engine based on JSON Queries. 
