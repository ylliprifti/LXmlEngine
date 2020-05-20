from bin.lxml_enginge.engine.JsonConfigReader import JsonConfigReader
import pytest


@pytest.fixture
def config_reader():
    return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/data-gather/bin/lxml_enginge/test/trader.extract.json")


@pytest.fixture
def ex_config_reader():
    with pytest.raises(Exception):
        return JsonConfigReader("/Users/ylliprifti/OneDrive/Dev/data-gather/bin/lxml_enginge/test/NOFILE")


def test_reader(config_reader):
    assert len(config_reader.read()["doc"]) > 10


def test_no_file_reader(ex_config_reader):
    pass
