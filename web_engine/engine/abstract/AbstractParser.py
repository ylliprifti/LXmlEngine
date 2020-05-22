from web_engine.interfaces.Parser import Parser

from interface import implements
from lxml import html, etree
import requests
from urllib.parse import urljoin


class AbstractParser(implements(Parser)):

    def __init__(self):
        self.last_tree: etree = None
        self.last_element: html = None
        self.last_inner_element = None
        self.last_items: list = None
        self.last_url: str = None

    def get_items(self, value: str, html_element) -> list:
        xpath_result = html_element.xpath(value)
        result = list()
        for x in xpath_result:
            if type(x) == html.HtmlElement:
                result.append(x.text)
            else:
                result.append(x)

        self.last_items = result
        return self.last_items

    def get_doc_element(self, doc):
        '''
        get the html element from the url [doc]
        :param doc: the url to the page
        :return: html.from string content
        '''
        with requests.get(doc) as page:
            self.last_url = doc
            self.last_tree: etree = html.fromstring(page.content)
            return self.last_tree

    def get_element(self, html_element, xpath):
        self.last_element = html_element.xpath(xpath)
        return self.last_element

    def get_inner_element(self, element, actions=None):
        self.last_inner_element = html.fromstring(etree.tostring(element, pretty_print=True))
        return self.last_inner_element

    def make_absolute_url(self, url):
        return urljoin(self.last_url, url)

    def get_doc_element_by_actions(self, actions: list):
        raise Exception("LXML Parser does not support actions. Consider using Selenium Parser.")


