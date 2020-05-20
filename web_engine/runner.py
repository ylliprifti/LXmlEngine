import sys

from web_engine.engine.JsonConfigReader import JsonConfigReader
from web_engine.engine.LXmlEngine import LXmlEngine
from pprint import pprint as pp


def main(argv):
    conf = JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/data-gather/bin/web_engine/test/trader.extract.json")
    engine = LXmlEngine()
    query: dict = conf.read()
    result = engine.process(query)
    pp(result)


if __name__ == "__main__":
    main(sys.argv)

