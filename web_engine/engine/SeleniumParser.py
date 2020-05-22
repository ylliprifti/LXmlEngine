from web_engine.engine.abstract.AbstractParser import AbstractParser
from urllib.parse import urljoin
import re

from selenium import webdriver
from lxml import etree, html

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SeleniumParser(AbstractParser):

    def __init__(self):
        super().__init__()
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        self.driver = webdriver.Firefox(firefox_profile)
        self.driver.set_window_size(800, 600)

    def get_items(self, value: str, html_element) -> list:
        if type(html_element) is not html.HtmlElement:
            html_element = html.fromstring(html_element)
        xpath_result = html_element.xpath(value)
        result = list()
        for x in xpath_result:
            if type(x) == html.HtmlElement:
                result.append(x.text)
            else:
                result.append(x)

        self.last_items = result
        return self.last_items

    def get_doc_element_by_action(self, actions: list):
        self.execute_actions(actions)
        elem = self.driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        self.last_tree = source_code
        return self.last_tree

    def get_doc_element(self, doc):
        '''
        get the html element from the url [doc]
        :param doc: the url to the page
        :return: html.from string content
        '''
        self.driver.get(doc)
        elem = self.driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        self.last_url = doc
        self.last_tree = source_code
        return self.last_tree

    def get_element(self, html_element, xpath):
        l_html = html.fromstring(html_element)
        self.last_element = l_html.xpath(xpath)
        return self.last_element

    def get_inner_element(self, element, actions=None):
        self.last_inner_element = html.fromstring(etree.tostring(element, pretty_print=True))
        return self.last_inner_element

    def make_absolute_url(self, url):
        return urljoin(self.last_url, url)

    def execute_actions(self, actions: list):
        if actions is None or len(actions) == 0:
            return
        [self.execute_action(x) for x in actions]

    def execute_action(self, action):
        pattern = '{(.+?)}'
        matches = re.search(pattern, action)
        if not matches:
            return
        action_type = matches.group(1)
        action_xpath = re.sub(pattern, '', action)
        if action_type.rstrip() == 'click':
            wait = WebDriverWait(self.driver, 10)
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, action_xpath)))
            elem.click()

    def __del__(self):
        if self.driver is not None:
            try:
                self.driver.close()
            except Exception as ex:
                pass


