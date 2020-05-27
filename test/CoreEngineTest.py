from web_engine.engine.CoreEngine import CoreEngine

import pytest
from unittest.mock import Mock

parser = Mock()
parser.get_doc_element.return_value = "<html><body>Hello</body></html>"
parser.get_doc_element_by_filter.return_value = "<html><body>Hello</body></html>"
parser.get_element.return_value = []


@pytest.fixture
def engine(dict_config_reader):
    core_engine = CoreEngine(parser=parser, query=dict_config_reader, log=None, context=None)
    return core_engine


def test_main_process(engine):
    result = engine.process()
    assert engine.parser.get_doc_element.assert_called()
    assert engine.parser.get_doc_element_by_filter.assert_called()
    assert engine.parser.get_element.assert_called()
    assert result

