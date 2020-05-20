import sys
from bin.lxml_enginge.engine.JsonConfigReader import JsonConfigReader
from bin.lxml_enginge.engine.XPathEnginge import XPathEngine
from pprint import pprint as pp


def main(argv):
    conf = JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/data-gather/bin/lxml_enginge/test/trader.extract.json")
    enginge = XPathEngine()
    query: dict = conf.read()
    result = enginge.process(query)
    pp(result)


if __name__ == "__main__":
    main(sys.argv)

