from bin.lxml_enginge.engine.JsonConfigReader import JsonConfigReader
from bin.lxml_enginge.engine.LXmlEngine import LXmlEngine

import pytest

@pytest.fixture
def config_reader():
    return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/data-gather/bin/web_engine/test/trader.extract.json")


@pytest.fixture()
def engine():
    return LXmlEngine()


def test_main_process(config_reader, engine):
    result = engine.process(config_reader.read())
    assert result is not None and result["data"] is not None

