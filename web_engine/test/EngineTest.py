from web_engine.engine.JsonQuery import JsonConfigReader
from web_engine.engine.CoreEngine import CoreEngine

from pprint import pprint as pp

import pytest


@pytest.fixture
def config_reader():
    return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/open-source/dr-web-engine/web_engine/test/trader.extract"
                            ".json")


@pytest.fixture()
def engine():
    return CoreEngine()


def test_main_process(config_reader, engine):
    result = engine.process(config_reader.load())
    pp(result)
    assert result is not None and result["data"] is not None

