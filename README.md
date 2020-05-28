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
using `pip3 install dr-web-engine` or integrating with the tools command line interface by running `web_engine/runner.py`
