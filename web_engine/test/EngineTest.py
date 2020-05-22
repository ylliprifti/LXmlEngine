from web_engine.engine.JsonConfigReader import JsonConfigReader
from web_engine.engine.ScrapEngine import ScrapEngine

from pprint import pprint as pp

import pytest


@pytest.fixture
def config_reader():
    return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/open-source/dr-web-engine/web_engine/test/trader.extract"
                            ".json")


@pytest.fixture()
def engine():
    return ScrapEngine()


def test_main_process(config_reader, engine):
    result = engine.process(config_reader.read())
    pp(result)
    assert result is not None and result["data"] is not None

