from web_engine.interfaces.Engine import Engine
from web_engine.interfaces.Parser import Parser

from interface import implements

import logging
import re


class ScrapEngine(implements(Engine)):

    def __init__(self, parser: Parser, log_level: int):
        logging.basicConfig(level=log_level)
        self.parser = parser
        self.log = logging.getLogger('Engine')

    def process(self, process_tree: dict) -> dict:
        if 'doc' not in process_tree.keys():
            self.log.info("XPathEngine::process -> doc was none")
            return None
        doc = process_tree['doc']
        result = self.__process(process_tree, self.parser.get_doc_element(doc))
        return result

    def __process(self, process_tree, html_element) -> dict:
        result = dict()
        process_tree = ScrapEngine.__filter_process_tree(process_tree)
        self.log.info("XPathEngine::__process -> process_tree: {}".format(process_tree))

        for key, value in process_tree.items():
            self.log.info("XPathEngine::__process -> key, value {}, {}".format(key, value))
            type_value = type(value)
            self.log.info("XPathEngine::__process -> value type {}".format(type_value))

            if type_value == str:
                result.update(self.__process_item(key, value, html_element))
            if type_value == list:
                if result.get(key) is None:
                    result[key] = list()
                temp_return = self.__process_array(key, value[0], html_element)
                result[key].append(temp_return)
            if type_value == dict:
                result.update({key: self.__process(value, html_element)})

        self.log.info("XPathEngine::__process -> result {}".format(result))
        return result

    def __process_array(self, key, value, html_element) -> list:
        result = list()

        if "__base_path" not in value:
            self.log.warning("XPathEngine::__process_array -> __base_path was not present")
            return result

        # if "__key" not in value:
        #   self.log.warning("XPathEngine::__process_array -> __key was not present")
        #    return result

        xpath = value["__base_path"]
        self.log.info("XPathEngine::__process_array -> xpath {}".format(xpath))

        # key = value["__key"]
        # self.log.info("XPathEngine::__process_array -> key {}".format(key))

        if 'doc' in value.keys():
            self.log.info("XPathEngine::__process_array -> doc {}".format(value['doc']))
            html_element = self.parser.get_doc_element(doc=value['doc'])
            del value['doc']

        selector = self.parser.get_element(html_element, xpath)

        if len(selector) == 0:
            self.log.warning("XPathEngine::__process_array -> selector length was 0")
            return result

        for item in selector:
            self.log.info("XPathEngine::__process_array -> selector.item {}".format(item))
            # TODO: To implement logic for action per each item
            # post_action = value.get('__post_action', None)
            # if post_action is not None:
            #    self.parser.get_doc_element_by_actions([post_action])
            temp_elem = self.parser.get_inner_element(item)
            result.append(self.__process(value, temp_elem))

        if "__follow" in value.keys():

            next_url = self.parser.get_element(html_element, value["__follow"])

            if next_url is not None and len(next_url) > 0:

                if '__follow_action' in value.keys():
                    action = value['__follow_action']
                    next_html_element = self.parser.get_doc_element_by_action([action])
                    result.extend(self.__process_array(key, value, next_html_element))
                else:
                    next_url = self.parser.make_absolute_url(next_url[0])
                    next_html_element = self.parser.get_doc_element(next_url)
                    result.extend(self.__process_array(key, value, next_html_element))

        self.log.info("XPathEngine::__process_array -> return result {}".format(result))
        return result

    def __process_item(self, key, value, html_element):

        self.log.info("XPathEngine::__process_item -> input key,value {}".format(key, value))

        self.log.info("XPathEngine::__process_item -> input html_elements {}".format(html_element))

        result = self.parser.get_items(value, html_element)

        self.log.info("XPathEngine::__process_item -> return result {}".format(result))
        return {key: result}

    @staticmethod
    def __filter_process_tree(process_tree: dict) -> dict:
        keywords: list = ['doc', '__base_path', "__key", "__follow", "__follow_action", "__post_action"]
        return dict((k, v) for k, v in process_tree.items() if k not in keywords)

