from web_engine.engine.JsonQuery import JsonConfigReader
import pytest


@pytest.fixture
def config_reader():
    return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/open-source/dr-web-engine/web_engine/test/trader.extract"
                            ".json")


@pytest.fixture
def ex_config_reader():
    with pytest.raises(Exception):
        return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/data-gather/bin/web_engine/test/NOFILE")


def test_reader(config_reader):
    assert len(config_reader.load()["doc"]) > 10


def test_no_file_reader(ex_config_reader):
    pass
