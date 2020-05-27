from web_engine.engine.JsonQuery import JsonQuery
from web_engine.engine.CoreEngine import CoreEngine
from web_engine.engine.LxmlParser import LxmlParser
from web_engine.engine.SeleniumScraper import SeleniumScraper
from web_engine.engine.RequestScraper import RequestScraper
from web_engine.engine.config.ScraperConfig import ScraperConfig

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

parser.add_argument('-ht', '--height', type=int, nargs="?",
                    help="specify the browser window height (default is 800, only used with Selenium engine)",
                    action="store", dest="height", default=800
                    )

parser.add_argument('-wh', '--width', type=int, nargs="?",
                    help="specify the browser window width (default is 1280, only used with Selenium engine)",
                    action="store", dest="width", default=1280
                    )

parser.add_argument('-lat', '--lat', type=int, nargs="?",
                    help="Latitude (not specified by default)",
                    action="store", dest="lat")

parser.add_argument('-lon', '--lon', type=int, nargs="?",
                    help="Longitude (not specified by default)",
                    action="store", dest="lon")

parser.add_argument('-img', '--img', type=bool, nargs="?",
                    help="Load images",
                    action="store", dest="img")

parser.add_argument('-l', '--log', type=bool, nargs="?",
                    help='Set flag to True to see verbose logging output',
                    action="store", dest="log", default=False)

parser.add_argument('-xvfb', '--xvfb', type=bool, nargs="?",
                    help='Set flag to False to see Firefox when using Selenium engine',
                    action="store", dest="xvfb", default=False
                    )

sys.setrecursionlimit(1000)


def main(argv):
    args = parser.parse_args()
    log_level = logging.ERROR
    if args.log:
        log_level = logging.NOTSET

    logging.basicConfig(level=log_level)
    log = logging.getLogger('Engine')

    if args.query is None:
        parser.print_help()
        return

    query = JsonQuery(json_query_path=args.query)

    scraper = RequestScraper(log)
    if args.engine == 'selenium':
        scraper_config = ScraperConfig({"xvfb": args.xvfb,
                                        "lon": args.lon or None,
                                        "lat": args.lat or None,
                                        "width": args.width,
                                        "height": args.height,
                                        "img": 1 if args.img else 2
                                        })
        scraper = SeleniumScraper(log, scraper_config)

    html_parser = LxmlParser(scraper, log)

    engine = CoreEngine(html_parser, query, log)

    result = engine.process()

    pp(result)
    # print(json.dumps(result))


if __name__ == "__main__":

    sys.argv.append("-q")
    sys.argv.append("/Users/ylliprifti/OneDrive/Dev/open-source/dr-web-engine/web_engine/test/trader.extract.json")

    sys.argv.append("-l")
    sys.argv.append("true")

    # sys.argv.append("-wh")
    # sys.argv.append("640")

    # sys.argv.append("-ht")
    # sys.argv.append("640")

    # sys.argv.append("-lon")
    # sys.argv.append("20")

    # sys.argv.append("-lat")
    # sys.argv.append("20")

    sys.argv.append("-img")
    sys.argv.append("True")

    sys.argv.append("-e")
    sys.argv.append("selenium")

    main(sys.argv)

