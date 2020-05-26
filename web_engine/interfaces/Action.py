from interface import Interface
from interface import interface

import logging


class Action(Interface):
    """
    Implement this interface to support action on the scraping engine
    """

    @interface.default
    def __init__(self, receiver, log: logging = None):
        self._log = log
        self._receiver = receiver
        pass

    def execute(self, *args):
        pass




