from web_engine.engine.JsonConfigReader import JsonConfigReader
from web_engine.engine.ScrapEngine import ScrapEngine
from web_engine.engine.LxmlParser import LxmlParser
from web_engine.engine.SeleniumParser import SeleniumParser

from pprint import pprint as pp

import argparse
import sys
import logging
import json


parser = argparse.ArgumentParser(description='Web Scrap Engine for semi-structured web data retrieval using JSON '
                                             'query constructs')

# Required positional argument
parser.add_argument('-q', '--query', type=str,
                    help='JSON query', action="store", dest="query")

parser.add_argument('-e', '--engine', type=str, nargs="?",
                    help='Engine: use [lxml] for parser engine (default), [selenium] for action based web scraping',
                    action="store", dest="engine", default="selenium")

parser.add_argument('-l', '--log', type=bool, nargs="?",
                    help='Set flag to True to see verbose logging output',
                    action="store", dest="log", default=False)

sys.setrecursionlimit(1000)


def main(argv):
    args = parser.parse_args()
    log_level = logging.ERROR
    if args.log:
        log_level = logging.NOTSET

    if args.query is None:
        parser.print_help()
        return

    conf = JsonConfigReader(args.query)

    engine_parser = SeleniumParser()
    if args.engine == 'lxml':
        engine_parser = LxmlParser()

    engine = ScrapEngine(log_level=log_level, parser=engine_parser)

    query: dict = conf.read()
    result = engine.process(query)
    print(json.dumps(result))


if __name__ == "__main__":
    sys.argv.append("-q")
    sys.argv.append("/Users/ylliprifti/OneDrive/Dev/open-source/dr-web-engine/web_engine/test/trader.extract.json")

    # sys.argv.append("-l")
    # sys.argv.append("true")

    sys.argv.append("-e")
    sys.argv.append("selenium")

    main(sys.argv)

