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

XVFB only works on Linux and the parameter is provided on a Windows or MacOX system you will get an error message. 

## Usage

To use the integrated CLI run `python3 -m webengine.runner`. This will display the following help message: 

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




