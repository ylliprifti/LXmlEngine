from typing import Dict, Any

from bin.lxml_enginge.interfaces.Engine import Engine
from interface import implements
from lxml import html, etree
import requests
import sys
import logging

logging.basicConfig(level=logging.NOTSET)

log = logging.getLogger('XPathEngine')

sys.setrecursionlimit(1000)


class XPathEngine(implements(Engine)):

    def process(self, process_tree: dict) -> dict:
        if 'doc' not in process_tree.keys():
            log.info("XPathEngine::process -> doc was none")
            return None
        return XPathEngine.__process(process_tree, XPathEngine.__get_element(process_tree['doc']))

    @staticmethod
    def __process(process_tree, html_element) -> dict:
        result = dict()

        process_tree = XPathEngine.__filter_process_tree(process_tree)
        log.info("XPathEngine::__process -> process_tree: {}".format(process_tree))

        for key, value in process_tree.items():
            log.info("XPathEngine::__process -> key, value {}, {}".format(key, value))
            type_value = type(value)
            log.info("XPathEngine::__process -> value type {}".format(type_value))

            if type_value == str:
                result.update(XPathEngine.__process_item(key, value, html_element))
            if type_value == list:
                temp_return = XPathEngine.__process_array(key, value[0], html_element)
                result.update({key: temp_return})
            if type_value == dict:
                result.update({key: XPathEngine.__process(value, html_element)})

        log.info("XPathEngine::__process -> result {}".format(result))
        return result

    @staticmethod
    def __process_array(key, value, html_element) -> list:
        result = list()

        if "__basepath" not in value:
            log.warning("XPathEngine::__process_array -> __basepath was not present")
            return result

        if "__key" not in value:
            log.warning("XPathEngine::__process_array -> __key was not present")
            return result

        xpath = value["__basepath"]
        log.info("XPathEngine::__process_array -> xpath {}".format(xpath))

        key = value["__key"]
        log.info("XPathEngine::__process_array -> key {}".format(key))

        if 'doc' in value.keys():
            log.info("XPathEngine::__process_array -> doc {}".format(value['doc']))
            html_element = XPathEngine.__get_element(value['doc'])

        selector = html_element.xpath(xpath)

        if len(selector) == 0:
            log.warning("XPathEngine::__process_array -> selector length was 0")
            return result

        for item in selector:
            log.info("XPathEngine::__process_array -> selector.item {}".format(item))
            temp_elem = html.fromstring(etree.tostring(item, pretty_print=True))
            result.append({key: XPathEngine.__process(value, temp_elem)})

        log.info("XPathEngine::__process_array -> return result {}".format(result))
        return result

    @staticmethod
    def __process_item(key, value, html_elements):

        log.info("XPathEngine::__process_item -> input key,value {}".format(key, value))

        log.info("XPathEngine::__process_item -> input html_elements {}".format(html_elements))

        xpath_result = html_elements.xpath(value)
        result = list()
        for x in xpath_result:
            if type(x) == html.HtmlElement:
                result.append(x.text)
            else:
                result.append(x)

        log.info("XPathEngine::__process_item -> return result {}".format(result))
        return {key: result}

    @staticmethod
    def __filter_process_tree(process_tree: dict) -> dict:
        keywords: list = ['doc', '__basepath', "__key"]
        return dict((k, v) for k, v in process_tree.items() if k not in keywords)

    @staticmethod
    def __get_element(doc):
        with requests.get(doc) as web_request:
            elements = html.fromstring(web_request.content)
            return elements


